import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def conn_db():
    """
    Establishes a connection to the SQL Server database using credentials 
    loaded from environment variables using dotenv.

    Returns:
        pyodbc.Connection or None: Returns the established connection or None if there's an error.
    """
    server = os.getenv('SERVER')
    db_name = os.getenv('DATABASE')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    print(f'Attempting to connect to the database with: SERVER={server}, DATABASE={db_name}, USER={user}')

    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={db_name};'
            f'UID={user};'
            f'PWD={password}'
        )
        print('CONNECTION SUCCESSFUL')
        return connection
    except Exception as e:
        print('Connection error:', e)
        return None

connection = conn_db()

if connection:
    cursor = connection.cursor()
    cursor.execute('SELECT @@version')
    row = cursor.fetchone()
    if row:
        print('Server version:', row[0])
    cursor.close()
    connection.close()
