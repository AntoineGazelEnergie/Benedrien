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



# ---- Load credentials from acces.env ----
load_dotenv("acces.env")

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

# ---- Paths ----
requete_sql = "hfc_query.sql"

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


def load_hfc(date_hfc):
    """
    Run HFC query for a single date_hfc and return DataFrame.
    date_hfc: datetime.date or datetime.datetime
    """
    with engine.connect() as conn:

        conn.execute(text("SET LANGUAGE French;"))


        with open(requete_sql, "r", encoding="utf-8") as f:
            sql = text(f.read())

        params = {"price_date": date_hfc.strftime("%Y-%m-%d")}

        df = pd.read_sql_query(sql, conn, params=params)

    return df


if __name__ == "__main__":
    date_hfc = datetime(2025, 10, 31)
    date_hfc.strftime("%Y-%m-%d")

    df = load_hfc(date_hfc)

    print(df)
