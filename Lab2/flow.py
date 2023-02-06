import sys
import random
from typing import List
from datetime import date, timedelta

import pandas as pd
from pykrx import stock
from sqlalchemy import create_engine
from prefect import flow, task, get_run_logger

from settings import Settings


@task(name="Extract")
def extract(
    start_date: str = str(date.today() - timedelta(days=365 * 1)),
    end_date: str = str(date.today()),
    ticker: str = "005930",
):

    # Download Data
    df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
    return df


@task(name="Transform")
def transform(df, ticker: str = "005930"):

    # Preprocessing Data
    df["Ticker"] = ticker
    df = df.reset_index()
    df.columns = Settings.COLUMNS

    return df


def flipCoin():
    return random.choice([True, True])


@task(name="Load")
def load(df, table_name: str = "stock"):
    engine = create_engine(Settings.POSTGRES_HOST)

    if flipCoin():
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print("Data Insert Success")
    else:
        raise Exception("Data Insert Failed")


@flow(name="ETL")
def ETL(name):
    logger = get_run_logger()
    logger.info(f"{name} registered this task. ")

    df_list = extract()
    df = transform(df_list)
    load(df, "stock")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "DefaultName"
    ETL(name)
