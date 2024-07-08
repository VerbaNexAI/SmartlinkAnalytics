import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class DataConnection:
    server = os.getenv('SERVER')
    db_name = os.getenv('DATABASE')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    def __init__(self):
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
        print("Closing connection")
        self.cursor.close()
        self.conn.close()

    def read_sql_file(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            return file.read()

