import os
import shutil
import cv2
import base64
import logging
import pandas as pd
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, File, UploadFile, FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from model.sql_transactions import SQLTransactions
from ultralytics import YOLO
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from logic.controller import Controller

app = FastAPI()
controller = Controller()
sql_trans = SQLTransactions()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectContent(BaseModel):
    """
    Pydantic model for project content.
    
    Attributes:
        projects (list[str]): List of project names.
    """
    projects: list[str]

@app.get("/")
def root():
    """
    Root endpoint that returns a simple message.
    
    Returns:
        dict: A dictionary containing a message about where to find the projects or SDGs.
    """
    return {"projects": "Here you can find the projects or SDGs"}

@app.get("/api/project")
async def get_projects():
    """
    Endpoint to get active projects from the database.
    
    Returns:
        list: A list of unique active projects.
    
    Raises:
        HTTPException: If there is an error retrieving the projects.
    """
    try:
        projects = sql_trans.get_active_projects()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["name"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["name"])

    return unique_projects

@app.post("/api/view")
async def post_project_content(projects: ProjectContent) -> List[dict]:
    """
    Endpoint to post project content and get view data.
    
    Args:
        projects (ProjectContent): A Pydantic model containing a list of project names.
    
    Returns:
        list: A list of dictionaries with combined project and view data.
    
    Raises:
        HTTPException: If there is an error retrieving or processing the project data.
    """
    try:
        logging.info(f"Received projects: {projects}")
        project_data = projects
        projects_info = [sql_trans.get_project(p) for p in project_data]

        if projects_info:
            logging.info(f"Projects found: {projects_info}")
            result = sql_trans.get_view_data()
            data = sql_trans.create_text_label_df(result)

            df = pd.DataFrame(result)
            df_seleccionado = df[
                ['SP_Item2ID', 'GraphicOID', 'SP_DrawingID', 'Item1Location', 'IsApproved', 'InconsistencyStatus', 'Severity']]
            lista_resultado = df_seleccionado.to_dict(orient='records')
            combinado = []

            for original, seleccionado in zip(data, lista_resultado):
                if original['label'] == 'LABEL_0':
                    original['descripcion'] = "Consistent"
                elif original['label'] == 'LABEL_1':
                    original['Description'] = 'Inconsistent Property Value'
                combinado.append({**original, **seleccionado})

            logging.info(f"Combined result: {combinado}")
            return combinado
        else:
            logging.warning(f"Projects not found for: {projects}")
            raise HTTPException(status_code=404, detail="Projects not found")
    except HTTPException as http_exc:
        logging.error(f"HTTP exception occurred: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.post("/upload-image-sel", response_class=JSONResponse)
async def upload_images_sel(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload images for the SEL model.
    
    Args:
        files (List[UploadFile]): A list of files to upload.
    
    Returns:
        JSONResponse: A JSON response with the result of the upload.
    """
    model_path = r'config/data/models/model_spi.pt'
    response = controller.upload_images(model_path, files)
    return response

@app.post("/upload-image-spi", response_class=JSONResponse)
async def upload_image_spi(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload images for the SPI model.
    
    Args:
        files (List[UploadFile]): A list of files to upload.
    
    Returns:
        JSONResponse: A JSON response with the result of the upload.
    """
    model_path = r'config/data/models/model_spi.pt'
    response = controller.upload_images(model_path, files)
    return response

@app.post("/upload-image-s3d-mecanica", response_class=JSONResponse)
async def upload_image_s3d_macanica(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload images for the S3D Mecánica model.
    
    Args:
        files (List[UploadFile]): A list of files to upload.
    
    Returns:
        JSONResponse: A JSON response with the result of the upload.
    """
    model_path = r'config/data/models/modelo-s3d-mecanica.pt'
    response = controller.upload_images(model_path, files)
    return response

@app.post("/upload-image-s3d-instrumentacion", response_class=JSONResponse)
async def upload_image_s3d_instrumentaltacion(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload images for the S3D Instrumentación model.
    
    Args:
        files (List[UploadFile]): A list of files to upload.
    
    Returns:
        JSONResponse: A JSON response with the result of the upload.
    """
    model_path = r'config/data/models/modelo-s3d-ins.pt'
    response = controller.upload_images(model_path, files)
    return response

@app.post("/upload-image-s3d-civil", response_class=JSONResponse)
async def upload_image_s3d_civil(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload images for the S3D Civil model.
    
    Args:
        files (List[UploadFile]): A list of files to upload.
    
    Returns:
        JSONResponse: A JSON response with the result of the upload.
    """
    model_path = r'config/data/models/modelo-s3d-civil.pt'
    response = controller.upload_images(model_path, files)
    return response

@app.post("/upload-image-s3d-electrica", response_class=JSONResponse)
async def upload_image_s3d_electrica(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload images for the S3D Eléctrica model.
    
    Args:
        files (List[UploadFile]): A list of files to upload.
    
    Returns:
        JSONResponse: A JSON response with the result of the upload.
    """
    model_path = r'config/data/models/modelo-s3d-electrica.pt'
    response = controller.upload_images(model_path, files)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
