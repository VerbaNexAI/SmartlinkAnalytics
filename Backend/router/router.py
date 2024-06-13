import re
from fastapi import APIRouter, HTTPException
from config.db import connect_db
from pydantic import BaseModel
from model.projects import get_active_projects, get_inactive_projects_from_db
from typing import List

# Create a FastAPI router instance
router = APIRouter()

# Define the model for project content
class ProjectContent(BaseModel):
    project: str

# Root endpoint
@router.get("/")
def root():
    return {"projects": "Here you can find the projects or SDGs"}

# Endpoint to get active projects
@router.get("/api/project")
async def get_projects():
    """Retrieve and return active projects."""
    try:
        projects = get_active_projects()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    # Filter unique projects
    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["PROYECTO"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["PROYECTO"])

    return unique_projects

# Endpoint to get inactive projects
@router.get("/api/project/inactive")
async def get_inactive_projects():
    """Retrieve and return inactive projects."""
    try:
        projects = await get_inactive_projects_from_db() 
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    # Filter unique projects
    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["PROYECTO"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["PROYECTO"])

    return unique_projects

# Endpoint to get views
@router.post("/api/view")
async def post_project_content(project: ProjectContent) -> List[dict]:
    print(f"Project: {project.project}")

    connection = connect_db()
    if not connection:
        raise HTTPException(
            status_code=500, detail="Could not connect to the database"
        )

    cursor = connection.cursor()
    try:
        cursor.execute("""
                SELECT [PROYECTO], [ID], [FECHA-CREACION], [ESTADO]
                FROM [ODS].[dbo].['NOMBRES-PROYECTOS-2D$']
                WHERE [PROYECTO] = ? 
                AND [ESTADO] = 'activo';
        """, (project.project,))
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

    if projects:
        print(f"Projects found: {projects}")

        connection = connect_db()
        if not connection:
            raise HTTPException(
                status_code=500, detail="Could not connect to the database"
            )
        cursor = connection.cursor()
        try:
            cursor.execute("""
                DECLARE @nombreVista NVARCHAR(128) = 'Vistas';
                DECLARE @sql NVARCHAR(MAX);

                IF EXISTS (SELECT 1 FROM sys.views WHERE name = @nombreVista)
                BEGIN
                    SET @sql = 'SELECT * FROM [' + @nombreVista + ']';
                    EXEC sp_executesql @sql;
                END
                ELSE
                BEGIN
                    EXEC sp_executesql N'
                    CREATE VIEW dbo.Vistas AS
                    SELECT dbo.Clientes.Nombre, dbo.Clientes.ClienteID, dbo.Pedidos.PedidoID, dbo.Pedidos.Fecha, dbo.Pedidos.Monto
                    FROM dbo.Clientes
                    INNER JOIN dbo.Pedidos ON dbo.Clientes.ClienteID = dbo.Pedidos.ClienteID';
                    
                    SET @sql = 'SELECT * FROM [' + @nombreVista + ']';
                    EXEC sp_executesql @sql;
                END
            """)
            column_names = [column[0] for column in cursor.description]
            result = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error executing additional query: {str(e)}",
            )
        finally:
            cursor.close()
            connection.close()

        return result
    else:
        print(f"Project not found for: {project.project}")
        raise HTTPException(status_code=404, detail="Project not found")



@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return FileResponse(BytesIO(contents), media_type='image/jpeg', filename=file.filename)