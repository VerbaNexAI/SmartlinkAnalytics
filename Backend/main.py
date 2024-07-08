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
from model.sql_transactions import SQLTransactions, detectar_objetos
from ultralytics import YOLO
from datetime import datetime
from pydantic import BaseModel
from model.sql_transactions import SQLTransactions
from fastapi.middleware.cors import CORSMiddleware
from logic.controller import Controller

app = FastAPI()
controller = Controller()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"projects": "Here you can find the projects or SDGs"}


@app.get("/api/project")
async def get_projects():
    try:
        projects = SQLTransactions.sql_trans.get_active_projects()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["name"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["name"])

    return unique_projects


@app.get("/api/project/inactive")
async def get_inactive_projects(self):
    try:
        projects = await self.sql_trans.get_inactive_projects_from_db()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    unique_projects = []
    seen_projects = set()

    for project in projects:
        if project["PROYECTO"] not in seen_projects:
            unique_projects.append(project)
            seen_projects.add(project["PROYECTO"])

    return unique_projects


@app.post("/api/view")
async def post_project_content(projects: BaseModel) -> List[dict]:
    try:
        logging.info(f"Received projects: {projects}")
        project_data = projects.dict()["projects"]
        projects_info = [SQLTransactions.sql_trans.get_project(p) for p in project_data]

        if projects_info:
            logging.info(f"Projects found: {projects_info}")
            result = SQLTransactions.sql_trans.get_view_data()
            data = SQLTransactions.sql_trans.create_text_label_df(result)

            df = pd.DataFrame(result)
            df_seleccionado = df[
                ['SP_Item2ID', 'GraphicOID', 'SP_DrawingID', 'Item1Location', 'IsApproved', 'InconsistencyStatus',
                 'Severity']]
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
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        processed_images = []
        detections = []

        for file in files:
            file_path = os.path.join(upload_folder, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded image: {file.filename}")

            model_path = r'config/data/models/model_pid.pt'
            model = YOLO(model_path)
            img = cv2.imread(file_path)
            if img is None:
                raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

            predictions = model.predict(img)
            output_img = predictions[0].plot()

            retval, buffer = cv2.imencode('.jpg', output_img)
            if not retval:
                raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

            print(f"Image {file.filename} processed and encoded successfully")
            encoded_img = base64.b64encode(buffer).decode('utf-8')
            detections.extend(detectar_objetos(model, [file_path]))
            fecha_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_empresa = 'SERINGTEC'

            processed_images.append({
                "filename": file.filename,
                "image_base64": encoded_img,
                "Fecha de Generación": fecha_generacion,
                "Empresa": nombre_empresa,
                "Detecciones": detections
            })

        return JSONResponse(content=processed_images)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/upload-image-spi", response_class=JSONResponse)
async def upload_image_spi(files: List[UploadFile] = File(...)):
    # controller.upload_images()
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        processed_images = []
        detections = []

        for file in files:
            file_path = os.path.join(upload_folder, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded image: {file.filename}")

            model_path = r'config/data/models/model_pid.pt'
            model = YOLO(model_path)
            img = cv2.imread(file_path)
            if img is None:
                raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

            predictions = model.predict(img)
            output_img = predictions[0].plot()

            retval, buffer = cv2.imencode('.jpg', output_img)
            if not retval:
                raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

            print(f"Image {file.filename} processed and encoded successfully")
            encoded_img = base64.b64encode(buffer).decode('utf-8')
            detections.extend(detectar_objetos(model, [file_path]))
            fecha_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_empresa = 'SERINGTEC'

            processed_images.append({
                "filename": file.filename,
                "image_base64": encoded_img,
                "Fecha de Generación": fecha_generacion,
                "Empresa": nombre_empresa,
                "Detecciones": detections
            })

        return JSONResponse(content=processed_images)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/upload-image-s3d-mecanica", response_class=JSONResponse)
async def upload_image_s3d_macanica(files: List[UploadFile] = File(...)):
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        processed_images = []
        detections = []

        for file in files:
            file_path = os.path.join(upload_folder, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded image: {file.filename}")

            model_path = r'config/data/models/modelo-s3d-mecanica.pt'
            model = YOLO(model_path)
            img = cv2.imread(file_path)
            if img is None:
                raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

            predictions = model.predict(img)
            output_img = predictions[0].plot()

            retval, buffer = cv2.imencode('.jpg', output_img)
            if not retval:
                raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

            print(f"Image {file.filename} processed and encoded successfully")
            encoded_img = base64.b64encode(buffer).decode('utf-8')
            detections.extend(detectar_objetos(model, [file_path]))
            fecha_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_empresa = 'SERINGTEC'

            processed_images.append({
                "filename": file.filename,
                "image_base64": encoded_img,
                "Fecha de Generación": fecha_generacion,
                "Empresa": nombre_empresa,
                "Detecciones": detections
            })

        return JSONResponse(content=processed_images)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/upload-image-s3d-instrumentacion", response_class=JSONResponse)
async def upload_image_s3d_instrumentaltacion(files: List[UploadFile] = File(...)):
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        processed_images = []
        detections = []

        for file in files:
            file_path = os.path.join(upload_folder, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded image: {file.filename}")

            model_path = r'config/data/models/modelo-s3d-ins.pt'
            model = YOLO(model_path)
            img = cv2.imread(file_path)
            if img is None:
                raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

            predictions = model.predict(img)
            output_img = predictions[0].plot()

            retval, buffer = cv2.imencode('.jpg', output_img)
            if not retval:
                raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

            print(f"Image {file.filename} processed and encoded successfully")
            encoded_img = base64.b64encode(buffer).decode('utf-8')
            detections.extend(detectar_objetos(model, [file_path]))
            fecha_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_empresa = 'SERINGTEC'

            processed_images.append({
                "filename": file.filename,
                "image_base64": encoded_img,
                "Fecha de Generación": fecha_generacion,
                "Empresa": nombre_empresa,
                "Detecciones": detections
            })

        return JSONResponse(content=processed_images)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/upload-image-s3d-civil", response_class=JSONResponse)
async def upload_image_s3d_civil(files: List[UploadFile] = File(...)):
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        processed_images = []
        detections = []

        for file in files:
            file_path = os.path.join(upload_folder, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded image: {file.filename}")

            model_path = r'config/data/models/modelo-s3d-civil.pt'
            model = YOLO(model_path)
            img = cv2.imread(file_path)
            if img is None:
                raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

            predictions = model.predict(img)
            output_img = predictions[0].plot()

            retval, buffer = cv2.imencode('.jpg', output_img)
            if not retval:
                raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

            print(f"Image {file.filename} processed and encoded successfully")
            encoded_img = base64.b64encode(buffer).decode('utf-8')
            detections.extend(detectar_objetos(model, [file_path]))
            fecha_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_empresa = 'SERINGTEC'

            processed_images.append({
                "filename": file.filename,
                "image_base64": encoded_img,
                "Fecha de Generación": fecha_generacion,
                "Empresa": nombre_empresa,
                "Detecciones": detections
            })

        return JSONResponse(content=processed_images)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/upload-image-s3d-electrica", response_class=JSONResponse)
async def upload_image_s3d_electrica(files: List[UploadFile] = File(...)):
    try:
        upload_folder = os.getenv('UPLOAD_FOLDER')
        os.makedirs(upload_folder, exist_ok=True)
        processed_images = []
        detections = []

        for file in files:
            file_path = os.path.join(upload_folder, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"Uploaded image: {file.filename}")

            model_path = r'config/data/models/modelo-s3d-electrica.pt'
            model = YOLO(model_path)
            img = cv2.imread(file_path)
            if img is None:
                raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

            predictions = model.predict(img)
            output_img = predictions[0].plot()

            retval, buffer = cv2.imencode('.jpg', output_img)
            if not retval:
                raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

            print(f"Image {file.filename} processed and encoded successfully")
            encoded_img = base64.b64encode(buffer).decode('utf-8')
            detections.extend(detectar_objetos(model, [file_path]))
            fecha_generacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_empresa = 'SERINGTEC'

            processed_images.append({
                "filename": file.filename,
                "image_base64": encoded_img,
                "Fecha de Generación": fecha_generacion,
                "Empresa": nombre_empresa,
                "Detecciones": detections
            })

        return JSONResponse(content=processed_images)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
