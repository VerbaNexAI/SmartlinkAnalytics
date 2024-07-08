import base64
import datetime
import os
import shutil
from msilib.schema import File
from typing import List
import cv2
from fastapi import HTTPException, UploadFile
from starlette.responses import JSONResponse
from ultralytics import YOLO


class Controller(object):

    def __init__(self):
        print("Load controller... test")

    def upload_images(self, files: List[UploadFile] = File(...)):
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
                # detections.extend(detectar_objetos(model, [file_path]))
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
