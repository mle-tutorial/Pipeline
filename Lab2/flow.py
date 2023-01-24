import sys
from typing import List
from datetime import date, timedelta

import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from prefect import flow, task, get_run_logger

from settings import Settings

@task(name="Extract")
def extract(
        start_date:str = str(date.today() - timedelta(days=365 * 1)),
        end_date:str = str(date.today()),
        tech_list:List[str] = ["AAPL", "GOOG", "MSFT", "AMZN"],
    ):

    # yfinance 데이터 download
    df_list = [
        yf.download(tech, start = start_date, end = end_date)
        for tech in tech_list
    ]

    return df_list

@task(name="Transform")
def transform(
        df_list,
        company_list:List[str] = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]
    ):
    for company, com_name in zip(df_list, company_list):
        company["company_name"] = com_name

    df = pd.concat(df_list, axis=0)

    df = df.reset_index(drop=False)

    return df

@task(name="Load")
def load(df, table_name):
    engine = create_engine(Settings.POSTGRES_HOST)

    df.to_sql(table_name, con=engine, if_exists="append", index=False)

@flow(name="ETL")
def ETL(name):
    logger = get_run_logger()
    logger.info(f"{name} registered this task. ")
    
    df_list = extract()
    df = transform(df_list)
    load(df, "stock")

if __name__ == "__main__":
    name = sys.argv[1]
    ETL()
    
