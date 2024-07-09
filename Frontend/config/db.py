import pyodbc
import os
from dotenv import load_dotenv


load_dotenv()

def conn_db():
    server = os.getenv('SERVER')
    bd_name = os.getenv('DATABASE')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    print(f'Intentando conectar a la base de datos con: SERVER={server}, DATABASE={bd_name}, USER={user}')

    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={bd_name};'
            f'UID={user};'
            f'PWD={password}'
        )
        print('CONEXION EXITOSA')
        return conexion
    except Exception as e:
        print('Error en la conexión:', e)
        return None

conexion = conn_db()




