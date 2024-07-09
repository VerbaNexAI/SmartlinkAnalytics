import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class DataConnection:
    """
    A class to manage a connection to a SQL Server database using pyodbc, 
    with credentials loaded from environment variables using dotenv.

    Attributes:
        server (str): The server name or IP address.
        db_name (str): The database name.
        user (str): The database username.
        password (str): The database password.
        conn (pyodbc.Connection): The connection object to interact with the database.
        cursor (pyodbc.Cursor): The cursor object to execute SQL queries.
    """

    server = os.getenv('SERVER')
    db_name = os.getenv('DATABASE')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    def __init__(self):
        """
        Initializes a connection to the SQL Server database using credentials 
        loaded from environment variables using dotenv.
        """
        print(f'Attempting to connect to the database with: SERVER={self.server}, DATABASE={self.db_name}, USER={self.user}')
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.server};'
                f'DATABASE={self.db_name};'
                f'UID={self.user};'
                f'PWD={self.password}'
            )
            self.cursor = self.conn.cursor()
            print('CONNECTION SUCCESSFUL')
        except Exception as e:
            print('Connection error:', e)

    def close(self):
        """
        Closes the database connection and cursor.
        """
        print("Closing connection")
        self.cursor.close()
        self.conn.close()

    def read_sql_file(self, file_path: str) -> str:
        """
        Reads the content of an SQL file.

        Args:
            file_path (str): The path to the SQL file.

        Returns:
            str: The content of the SQL file as a string.
        """
        with open(file_path, 'r') as file:
            return file.read()

# Example usage
if __name__ == "__main__":
    try:
        connection = DataConnection()
        query = connection.read_sql_file('path/to/sql/file.sql')
        connection.cursor.execute(query)
        rows = connection.cursor.fetchall()
        print("Query results:", rows)
    finally:
        if connection:
            connection.close()
