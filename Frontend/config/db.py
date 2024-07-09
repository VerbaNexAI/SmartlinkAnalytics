import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
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
        # Attempt to establish connection with provided credentials
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
        # Capture and handle connection errors
        print('Connection error:', e)
        return None

# Call the function to establish the connection
connection = conn_db()

# Example of executing a query after establishing the connection
if connection:
    cursor = connection.cursor()
    cursor.execute('SELECT @@version')
    row = cursor.fetchone()
    if row:
        print('Server version:', row[0])
    cursor.close()
    connection.close()  # It's important to close the connection when no longer needed
