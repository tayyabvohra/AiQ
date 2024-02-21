import pandas as pd
import requests
import pyodbc
from sqlalchemy import create_engine

# Replace the placeholders with your actual SQL Server connection details
def push_df_to_db(df,table_name):
    host = 'DESKTOP-6P1LUS8'
    database_name = 'AiQ'
    driver = 'SQL Server Native Client 11.0'
    connection_string = f"mssql+pyodbc://{host}/{database_name}?driver={driver}"
    engine = create_engine(connection_string)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    engine.dispose()
