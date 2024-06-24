import os
import shutil
import io
import cv2
from typing import List
from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from config.db import connect_db
from model.projects import get_active_projects, get_inactive_projects_from_db,get_project,get_view_data
from ultralytics import YOLO

# Create a FastAPI router instance
router = APIRouter()

class ProjectContent(BaseModel):
    """Model for project content.
    
    Attributes:
        project (str): The project name.
    """
    project: str

@router.get("/")
def root():
    """Root endpoint to return available projects or SDGs.

    :returns: A dictionary containing available projects or SDGs.
    :rtype: dict
    """
    return {"projects": "Here you can find the projects or SDGs"}

@router.get("/api/project")
async def get_projects():
    """Retrieve and return active projects.

    :returns: A list of unique active projects.
    :rtype: List[dict]
    :raises HTTPException: If there is an issue retrieving projects.
    """
    try:
        projects = get_active_projects()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["PROYECTO"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["PROYECTO"])

    return unique_projects

@router.get("/api/project/inactive")
async def get_inactive_projects():
    """Retrieve and return inactive projects.

    :returns: A list of unique inactive projects.
    :rtype: List[dict]
    :raises HTTPException: If there is an issue retrieving projects.
    """
    try:
        projects = await get_inactive_projects_from_db()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["PROYECTO"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["PROYECTO"])

    return unique_projects

@router.post("/api/view")
async def post_project_content(project: ProjectContent) -> List[dict]:
    """Retrieve views for a specific project.

    :param project: The project content model.
    :type project: ProjectContent
    :returns: A list of views related to the project.
    :rtype: List[dict]
    :raises HTTPException: If there is an issue connecting to the database or executing queries.
    """
    print(f"Project: {project.project}")

    projects = get_project(project.project)
    
    if projects:
        print(f"Projects found: {projects}")
        result = get_view_data()
        return result
    else:
        print(f"Project not found for: {project.project}")
        raise HTTPException(status_code=404, detail="Project not found")

@router.post("/upload-image", response_class=StreamingResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload an image, perform YOLO prediction, and return processed image.

    :param file: The uploaded image file.
    :type file: UploadFile
    :returns: A streaming response with the processed image in JPEG format.
    :rtype: StreamingResponse
    :raises HTTPException: If there is an issue with the image upload, reading, processing, or encoding.
    """
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("filename:", file.filename, "\nfile_path:", file_path)

        model_path = r'model/best.pt'
        model = YOLO(model_path)
        img = cv2.imread(file_path)
        if img is None:
            raise HTTPException(status_code=400, detail="Failed to read image")

        predictions = model.predict(img)
        output_img = predictions[0].plot()

        retval, buffer = cv2.imencode('.jpg', output_img)
        if not retval:
            raise HTTPException(status_code=500, detail="Failed to encode image")

        print("Image processed and encoded successfully")

        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/upload-image-s3d", response_class=StreamingResponse)
async def upload_image_s3d(file: UploadFile = File(...)):
    """Upload an image, perform YOLO prediction, and return processed image.

    :param file: The uploaded image file.
    :type file: UploadFile
    :returns: A streaming response with the processed image in JPEG format.
    :rtype: StreamingResponse
    :raises HTTPException: If there is an issue with the image upload, reading, processing, or encoding.
    """
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("filename:", file.filename, "\nfile_path:", file_path)

        model_path = r'model/best.pt'
        model = YOLO(model_path)
        img = cv2.imread(file_path)
        if img is None:
            raise HTTPException(status_code=400, detail="Failed to read image")

        predictions = model.predict(img)
        output_img = predictions[0].plot()

        retval, buffer = cv2.imencode('.jpg', output_img)
        if not retval:
            raise HTTPException(status_code=500, detail="Failed to encode image")

        print("Image processed and encoded successfully")

        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/upload-image-spi", response_class=StreamingResponse)
async def upload_image_spi(file: UploadFile = File(...)):
    """Upload an image, perform YOLO prediction, and return processed image.

    :param file: The uploaded image file.
    :type file: UploadFile
    :returns: A streaming response with the processed image in JPEG format.
    :rtype: StreamingResponse
    :raises HTTPException: If there is an issue with the image upload, reading, processing, or encoding.
    """
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print("filename:", file.filename, "\nfile_path:", file_path)

        model_path = r'model/best.pt'
        model = YOLO(model_path)
        img = cv2.imread(file_path)
        if img is None:
            raise HTTPException(status_code=400, detail="Failed to read image")

        predictions = model.predict(img)
        output_img = predictions[0].plot()

        retval, buffer = cv2.imencode('.jpg', output_img)
        if not retval:
            raise HTTPException(status_code=500, detail="Failed to encode image")

        print("Image processed and encoded successfully")

        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
