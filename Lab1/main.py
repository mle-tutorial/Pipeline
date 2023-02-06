import random
from datetime import date, timedelta

from pykrx import stock
from sqlalchemy import create_engine

from settings import Settings


def extract(
    start_date: str = str(date.today() - timedelta(days=365 * 1)),
    end_date: str = str(date.today()),
    ticker: str = "005930",
):

    # Download Data
    df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
    return df


def transform(df, ticker: str = "005930"):

    # Preprocessing Data
    df["Ticker"] = ticker
    df = df.reset_index()
    df.columns = Settings.COLUMNS

    return df


def flipCoin():
    return random.choice([True, False])


def load(df, table_name: str = "stock"):
    engine = create_engine(Settings.POSTGRES_HOST)

    if flipCoin():
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print("Data Insert Success")
    else:
        raise Exception("Data Insert Failed")


def ETL():
    df_list = extract()
    df = transform(df_list)
    load(df)


if __name__ == "__main__":
    ETL()
