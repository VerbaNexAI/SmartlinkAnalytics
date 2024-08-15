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
from pathlib import Path



class Controller(object):

    def __init__(self):
        print("Load controller... test")

    def upload_images(self, model_path, files: List[UploadFile]):
        """
        Upload and process images using a YOLO model.
        :param files: List of images to upload.
        :type files: List[UploadFile]
        :return: JSON response with processed image data.
        :rtype: JSONResponse
        :raises HTTPException: If there is an error during image upload or processing.
        """
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

                model = YOLO(model_path)
                img = cv2.imread(file_path)
                if img is None:
                    raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

                predictions = model.predict(img)
                output_img = predictions[0].plot(font_size=25)
                retval, buffer = cv2.imencode('.jpg', output_img)
                if not retval:
                    raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

                print(f"Image {file.filename} processed and encoded successfully")
                encoded_img = base64.b64encode(buffer).decode('utf-8')
                detections.extend(self.detectar_objetos(model, [file_path]))
                fecha_generacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                nombre_empresa = 'SERINGTEC'

                processed_images.append({
                    "filename": file.filename,
                    "image_base64": encoded_img,
                    "Fecha de Generación": fecha_generacion,
                    "Empresa": nombre_empresa,
                    "Detecciones": detections
                })

                archivo_a_eliminar = file_path
                if os.path.exists(archivo_a_eliminar):
                    os.remove(archivo_a_eliminar)
                    print("Archivo eliminado con éxito.")
                else:
                    print("El archivo no existe.")
                    
            return JSONResponse(content=processed_images)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        

    def detectar_objetos(self,model, image_paths):
        """
        Detect objects in the given images using the specified model.

        Args:
            model: The object detection model to use for predictions.
            image_paths (list): List of paths to the images to process.

        Returns:
            list: A list of dictionaries, each containing details of the detected objects.
            Each dictionary has the following keys:
                - 'Imagen': Name of the image file.
                - 'Clase': Detected object class.
                - 'Confianza': Confidence score of the detection.
                - 'Box_X1': X-coordinate of the top-left corner of the bounding box.
                - 'Box_Y1': Y-coordinate of the top-left corner of the bounding box.
                - 'Box_X2': X-coordinate of the bottom-right corner of the bounding box.
                - 'Box_Y2': Y-coordinate of the bottom-right corner of the bounding box.
        """
        detections = []
        for img_path in image_paths:
            results = model(img_path)  
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy() 
                confidences = result.boxes.conf.cpu().numpy()  
                classes = result.boxes.cls.cpu().numpy()  
                for box, conf, cls in zip(boxes, confidences, classes):
                    detections.append({
                        'Imagen': Path(img_path).name,
                        'Clase': model.names[int(cls)],
                        'Confianza': float(conf),
                        'Box_X1': float(box[0]),
                        'Box_Y1': float(box[1]),
                        'Box_X2': float(box[2]),
                        'Box_Y2': float(box[3])
                    })
        return detections
