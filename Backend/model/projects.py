import pyodbc
from fastapi import HTTPException
from config.db import connect_db
from typing import List, Dict

def read_sql_file(file_path):
    """Reads the contents of a SQL file."""
    with open(file_path, 'r') as file:
        return file.read()


def get_active_projects():
    """Retrieve active projects from the database."""
    connection = connect_db()
    if not connection:
        raise HTTPException(
            status_code=500, detail="Could not connect to the database"
        )

    cursor = connection.cursor()
    try:
        # Leer el archivo .sql
        sql_query = read_sql_file(r'config\data\project-active.sql')
        
        # Ejecutar la consulta desde el archivo .sql
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        projects = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al ejecutar la consulta: {str(e)}"
        )
    finally:
        cursor.close()
        connection.close()

    return projects

async def get_inactive_projects_from_db():
    """Retrieve inactive projects from the database."""
    try:
        connection = connect_db()
        if not connection:
            raise HTTPException(
                status_code=500, detail="Could not connect to the database"
            )

        cursor = connection.cursor()
        try:
            # Leer el archivo .sql
            sql_query = read_sql_file(r'config\data\project-inactve.sql')
            
            # Ejecutar la consulta desde el archivo .sql
            cursor.execute(sql_query)

            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            projects = [dict(zip(columns, row)) for row in rows]
            return projects
        finally:
            cursor.close()
            connection.close()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al ejecutar la consulta: {str(e)}"
        )



def get_project(project_name: str) -> List[Dict]:
    """Retrieve projects from the database based on project name."""
    connection = connect_db()
    if not connection:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    
    cursor = connection.cursor()
    try:
        # Leer el archivo .sql
        sql_query = read_sql_file(r'config\data\project.sql')
        
        # Ejecutar la consulta desde el archivo .sql
        cursor.execute(sql_query, (project_name,))
        
        # Obtener los nombres de las columnas y los resultados
        columns = [column[0] for column in cursor.description]
        projects = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing the query: {str(e)}")
    finally:
        cursor.close()
        connection.close()

def get_view_data() -> List[Dict]:
    """Retrieve view data from the database or create the view if it does not exist."""
    connection = connect_db()
    if not connection:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    
    cursor = connection.cursor()
    try:
        # Leer el archivo .sql
        sql_query = read_sql_file(r'config\data\view.sql')
        
        # Ejecutar la consulta desde el archivo .sql
        cursor.execute(sql_query)
        
        # Obtener los nombres de las columnas y los resultados
        column_names = [column[0] for column in cursor.description]
        result = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing additional query: {str(e)}")
    finally:
        cursor.close()
        connection.close()