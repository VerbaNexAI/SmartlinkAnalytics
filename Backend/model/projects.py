import pyodbc
from fastapi import HTTPException
from config.db import connect_db

def get_active_projects():
    """Retrieve active projects from the database."""
    connection = connect_db()
    if not connection:
        raise HTTPException(
            status_code=500, detail="Could not connect to the database"
        )

    cursor = connection.cursor()
    try:
        # Execute the query to get active projects
        cursor.execute("""
            SELECT [PROYECTO], [ID], [FECHA-CREACION], [ESTADO]
            FROM [ODS].[dbo].['NOMBRES-PROYECTOS-2D$']
            WHERE [PROYECTO] NOT LIKE '%SBD%' AND
                  [ESTADO] = 'activo';
        """)
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
            # Execute the query to get inactive projects
            cursor.execute("""
                SELECT [PROYECTO], [ID], [FECHA-CREACION], [ESTADO]
                FROM [ODS].[dbo].['NOMBRES-PROYECTOS-2D$']
                WHERE [PROYECTO] NOT LIKE '%SBD%'
                AND [PROYECTO] NOT LIKE '%master%'
                AND [PROYECTO] NOT LIKE '%tempdb%'
                AND [PROYECTO] NOT LIKE '%model%'
                AND [PROYECTO] NOT LIKE '%msdb%'
                AND [PROYECTO] NOT LIKE '%CAS05%'
                AND [ESTADO] = 'inactivo';
            """)

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


