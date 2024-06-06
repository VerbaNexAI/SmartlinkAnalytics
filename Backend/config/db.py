import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def connect_db():
    """Attempt to connect to the database using environment variables."""
    server = os.getenv('SERVER')
    db_name = os.getenv('DATABASE')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    print(f'Attempting to connect to the database with: SERVER={server}, DATABASE={db_name}, USER={user}')

    try:
        # Establish a connection to the database
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

# Establish a connection to the database
connection = connect_db()
