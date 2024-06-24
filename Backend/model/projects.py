import pyodbc
from fastapi import HTTPException
from config.db import connect_db
from typing import List, Dict

def read_sql_file(file_path):
    """Reads the contents of a SQL file."""
    with open(file_path, 'r') as file:
        return file.read()


def get_active_projects():
    """
    Retrieve active projects from the database.

    :returns: A list of active projects.
    :rtype: List[Dict]
    :raises HTTPException: If there is an issue connecting to the database or executing queries.
    """
    connection = connect_db()
    if not connection:
        raise HTTPException(
            status_code=500, detail="Could not connect to the database"
        )

    cursor = connection.cursor()
    try:
        # Read the .sql file
        sql_query = read_sql_file(r'config\data\project-active.sql')
        
        # Execute the query from the .sql file
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        projects = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error executing the query: {str(e)}"
        )
    finally:
        cursor.close()
        connection.close()

    return projects

async def get_inactive_projects_from_db():
    """
    Retrieve inactive projects from the database asynchronously.

    :returns: A list of inactive projects.
    :rtype: List[Dict]
    :raises HTTPException: If there is an issue connecting to the database or executing queries.
    """
    try:
        connection = connect_db()
        if not connection:
            raise HTTPException(
                status_code=500, detail="Could not connect to the database"
            )

        cursor = connection.cursor()
        try:
            # Read the .sql file
            sql_query = read_sql_file(r'config\data\project-inactve.sql')
            
            # Execute the query from the .sql file
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
            status_code=500, detail=f"Error executing the query: {str(e)}"
        )


def get_project(project_name: str) -> List[Dict]:
    """
    Retrieve projects from the database based on project name.

    :param project_name: The name of the project to retrieve.
    :type project_name: str
    :returns: A list of projects matching the project name.
    :rtype: List[Dict]
    :raises HTTPException: If there is an issue connecting to the database or executing queries.
    """
    connection = connect_db()
    if not connection:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    
    cursor = connection.cursor()
    try:
        # Read the .sql file
        sql_query = read_sql_file(r'config\data\project.sql')
        
        # Execute the query from the .sql file
        cursor.execute(sql_query, (project_name,))
        
        # Get column names and results
        columns = [column[0] for column in cursor.description]
        projects = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing the query: {str(e)}")
    finally:
        cursor.close()
        connection.close()

def get_view_data() -> List[Dict]:
    """
    Retrieve view data from the database or create the view if it does not exist.

    :returns: A list of data from the view.
    :rtype: List[Dict]
    :raises HTTPException: If there is an issue connecting to the database or executing queries.
    """
    connection = connect_db()
    if not connection:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    
    cursor = connection.cursor()
    try:
        # Read the .sql file
        sql_query = read_sql_file(r'config\data\view.sql')
        
        # Execute the query from the .sql file
        cursor.execute(sql_query)
        
        # Get column names and results
        column_names = [column[0] for column in cursor.description]
        result = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing additional query: {str(e)}")
    finally:
        cursor.close()
        connection.close()
