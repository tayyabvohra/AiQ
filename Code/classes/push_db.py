import pandas as pd
from sqlalchemy import create_engine

# Replace the placeholders with your actual SQL Server connection details
def push_df_to_db(df, table_name):
    host = 'tayyabvohra'
    database_name = 'test_db'
    trusted_connection='yes'
    # Construct the connection string with the ODBC driver specified
    driver = 'ODBC Driver 17 for SQL Server'  # Adjust the driver name as per your installation
    conn_str = f'mssql+pyodbc://{host}/{database_name}?trusted_connection={trusted_connection}&driver={driver}'
    engine = create_engine(conn_str)
    
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"DataFrame successfully pushed to {table_name} in {database_name}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        engine.dispose()

