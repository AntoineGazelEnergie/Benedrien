# -*- coding: utf-8 -*-
"""
Created on Wed Nov 05 2025
@author: You
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from datetime import datetime, timedelta
from dotenv import load_dotenv
import matplotlib.pyplot as plt


# ---- Load credentials from acces.env ----
load_dotenv("acces.env")

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

# ---- Paths ----
requete_sql = "spot_query.sql"

# ---- Build SQLAlchemy connection ----
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;TrustServerCertificate=no;"
)
conn_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})
engine = create_engine(conn_url)


def load_spot(start_date: datetime, end_date: datetime):
    """Run EPEX spot query and return pandas DataFrame."""
    with open(requete_sql, "r", encoding="utf-8") as f:
        sql = text(f.read())

    params = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
    }

    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params=params)

 
    return df


if __name__ == "__main__":
    start_date = datetime(2025, 10, 1)
    end_date = datetime(2025, 11, 10)

    df = load_spot(start_date, end_date)

    print(df.head())
