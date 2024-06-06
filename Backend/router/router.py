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
    tool: str

# Function to process project names
def process_string(string):
    # Remove the "_SDB" suffix if present
    without_sdb = re.sub(r"_SDB$", "", string)
    # Search for a substring starting with "ECO"
    eco = re.search(r"ECO.*", without_sdb)
    if eco:
        return eco.group(0)
    return without_sdb

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

    # Process project names
    for project in projects:
        project["PROYECTO"] = process_string(project["PROYECTO"])

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

    # Process project names
    for project in projects:
        project["PROYECTO"] = process_string(project["PROYECTO"])

    # Filter unique projects
    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["PROYECTO"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["PROYECTO"])

    return unique_projects

@router.post("/api/view")
async def post_project_content(project: ProjectContent) -> List[dict]:
    # Imprimir los datos recibidos
    print(f"Project: {project.project}")
    print(f"Tool: {project.tool}")

    # Get active projects data
    projects_data = get_active_projects()

    # Find matching project
    matching_project = None
    for proj in projects_data:
        if project.project in proj["PROYECTO"]:
            matching_project = proj
            break

    if matching_project:
        print(f"Project found: {matching_project}")

        connection = connect_db()
        if not connection:
            raise HTTPException(
                status_code=500, detail="Could not connect to the database"
            )
        cursor = connection.cursor()
        try:
            # Aquí puedes utilizar tanto el proyecto como la herramienta en tu lógica de negocio
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
