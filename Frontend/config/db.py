import pyodbc
import os
from dotenv import load_dotenv


load_dotenv()

def conn_db():
    server = os.getenv('SERVER')
    bd_name = os.getenv('DATABASE')
    usuario = os.getenv('USER')
    contraseña = os.getenv('PASSWORD')

    print(f'Intentando conectar a la base de datos con: SERVER={server}, DATABASE={bd_name}, USER={usuario}')

    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={bd_name};'
            f'UID={usuario};'
            f'PWD={contraseña}'
        )
        print('CONEXION EXITOSA')
        return conexion
    except Exception as e:
        print('Error en la conexión:', e)
        return None

conexion = conn_db()




