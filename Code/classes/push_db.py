import pandas as pd
import requests
import pyodbc
from sqlalchemy import create_engine

# Replace the placeholders with your actual SQL Server connection details
def push_df_to_db(df,table_name):
    host = 'tayyabvohra'
    database_name = 'test_db'
    driver = 'ODBC Driver 17 for SQL Server'
    connection_string = f"mssql+pyodbc://{host}/{database_name}?driver={driver}"
    engine = create_engine(connection_string)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    engine.dispose()