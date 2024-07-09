import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def conn_db():
    """
    Establece una conexión a la base de datos SQL Server utilizando las credenciales 
    cargadas desde variables de entorno utilizando dotenv.

    Returns:
        pyodbc.Connection or None: Retorna la conexión establecida o None si hay un error.
    """
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

if conexion:
    cursor = conexion.cursor()
    cursor.execute('SELECT @@version')
    row = cursor.fetchone()
    if row:
        print('Versión del servidor:', row[0])
    cursor.close()
    conexion.close() 
