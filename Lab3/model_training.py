import sys
from datetime import datetime, timedelta

import pandas as pd
from prefect import flow, task, get_run_logger
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_squared_log_error,
    mean_absolute_error,
    mean_squared_error,
)

from settings import Settings


@task(name="create_engine")
def create_db_engine(HOST_URL):
    engine = create_engine(HOST_URL)
    return engine


@task(name="read_data")
def read_data_from_database(query, engine):
    return pd.read_sql_query(query, con=engine)


@task(name="preprocess_data")
def preprocessing(train_df, valid_df, basedate):
    features = ["Open", "High", "Low", "Close", "Volume"]
    scaler = MinMaxScaler()

    df = pd.concat([train_df, valid_df], axis=0, ignore_index=True)
    df["TomorrowClosePrice"] = df["Close"].shift(-1)

    idx = int(df[df["Date"] == basedate].index[0])

    train_df = df.iloc[: idx + 1].copy().reset_index()
    valid_df = df.iloc[idx + 1 :].copy().reset_index()

    train_feature_df = train_df[features]

    train_X = scaler.fit_transform(train_feature_df)
    train_Y = train_df["TomorrowClosePrice"]

    valid_Y = valid_df["Close"].shift(-1)
    valid_Y.rename("TomorrowClosePrice", inplace=True)
    valid_feature_df = valid_df[features]
    valid_X = scaler.transform(valid_feature_df)

    return train_X, train_Y, valid_X, valid_Y


@task(name="train_model")
def train_model(train_X, train_Y):
    model = LinearRegression()
    model.fit(train_X, train_Y)

    return model


@task(name="make_score")
def make_score(model, valid_X, valid_Y):
    pred = pd.Series(model.predict(valid_X))
    df = pd.concat([valid_Y, pred], axis=1, ignore_index=True)
    df.columns = ["TomorrowClosePrice", "PredictionResult"]
    df.dropna(inplace=True)

    msle = mean_squared_log_error(df["TomorrowClosePrice"], df["PredictionResult"])
    mae = mean_absolute_error(df["TomorrowClosePrice"], df["PredictionResult"])
    mse = mean_squared_error(df["TomorrowClosePrice"], df["PredictionResult"])

    info_dict = {
        "msle": msle,
        "mae": mae,
        "mse": mse,
    }

    return info_dict


@task(name="save_data")
def save_data(*args):
    logger = get_run_logger()
    for arg in args:
        logger.info(arg)


@flow(name="stock_data_train")
def training_flow(basedate):
    if basedate == "daily":  # 평일만 basedate로 사용하는 로직
        basedate = (datetime.today() + timedelta(hours=9) - timedelta(days=30)).date()
        while not basedate.weekday() < 5:
            basedate -= timedelta(days=1)
        basedate = str(basedate)

    HOST_URL = Settings.POSTGRES_HOST
    TABLE_NAME = "stock"
    TRAIN_QUERY = f"""
        SELECT * FROM {TABLE_NAME} WHERE "Date" < '{basedate}'
    """
    VALID_QUERY = f"""
        SELECT * FROM {TABLE_NAME} WHERE "Date" >= '{basedate}' 
    """

    engine = create_db_engine(HOST_URL)
    train_df = read_data_from_database(TRAIN_QUERY, engine)
    valid_df = read_data_from_database(VALID_QUERY, engine)
    train_X, train_Y, valid_X, valid_Y = preprocessing(train_df, valid_df, basedate)
    model = train_model(train_X, train_Y)
    score_dict = make_score(model, valid_X, valid_Y)
    save_data(basedate, score_dict)


if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else "daily"

    training_flow(date)
