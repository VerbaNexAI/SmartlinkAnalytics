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



# class Controller(object):

#     def __init__(self):
#         print("Load controller... test")

#     def upload_images(self, model_path, files: List[UploadFile]):
#         """
#         Upload and process images using a YOLO model.
#         :param files: List of images to upload.
#         :type files: List[UploadFile]
#         :return: JSON response with processed image data.
#         :rtype: JSONResponse
#         :raises HTTPException: If there is an error during image upload or processing.
#         """
#         try:
#             upload_folder = os.getenv('UPLOAD_FOLDER')
#             os.makedirs(upload_folder, exist_ok=True)
#             processed_images = []
#             detections = []

#             for file in files:
#                 file_path = os.path.join(upload_folder, file.filename)

#                 with open(file_path, "wb") as buffer:
#                     shutil.copyfileobj(file.file, buffer)
#                 print(f"Uploaded image: {file.filename}")

#                 model = YOLO(model_path)
#                 img = cv2.imread(file_path)
#                 if img is None:
#                     raise HTTPException(status_code=400, detail=f"Failed to read image: {file.filename}")

#                 predictions = model.predict(img)
#                 output_img = predictions[0].plot(font_size=12, line_width=3, labels=True, conf=True)
#                 retval, buffer = cv2.imencode('.jpg', output_img)
#                 if not retval:
#                     raise HTTPException(status_code=500, detail=f"Failed to encode image: {file.filename}")

#                 print(f"Image {file.filename} processed and encoded successfully")
#                 encoded_img = base64.b64encode(buffer).decode('utf-8')
#                 detections.extend(self.detectar_objetos(model, [file_path]))
#                 fecha_generacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 nombre_empresa = 'SERINGTEC'

#                 processed_images.append({
#                     "filename": file.filename,
#                     "image_base64": encoded_img,
#                     "Fecha de Generación": fecha_generacion,
#                     "Empresa": nombre_empresa,
#                     "Detecciones": detections
#                 })

#                 archivo_a_eliminar = file_path
#                 if os.path.exists(archivo_a_eliminar):
#                     os.remove(archivo_a_eliminar)
#                     print("Archivo eliminado con éxito.")
#                 else:
#                     print("El archivo no existe.")
                    
#             return JSONResponse(content=processed_images)
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        

#     def detectar_objetos(self,model, image_paths):
#         """
#         Detect objects in the given images using the specified model.

#         Args:
#             model: The object detection model to use for predictions.
#             image_paths (list): List of paths to the images to process.

#         Returns:
#             list: A list of dictionaries, each containing details of the detected objects.
#             Each dictionary has the following keys:
#                 - 'Imagen': Name of the image file.
#                 - 'Clase': Detected object class.
#                 - 'Confianza': Confidence score of the detection.
#                 - 'Box_X1': X-coordinate of the top-left corner of the bounding box.
#                 - 'Box_Y1': Y-coordinate of the top-left corner of the bounding box.
#                 - 'Box_X2': X-coordinate of the bottom-right corner of the bounding box.
#                 - 'Box_Y2': Y-coordinate of the bottom-right corner of the bounding box.
#         """
#         detections = []
#         for img_path in image_paths:
#             results = model(img_path)  
#             for result in results:
#                 boxes = result.boxes.xyxy.cpu().numpy() 
#                 confidences = result.boxes.conf.cpu().numpy()  
#                 classes = result.boxes.cls.cpu().numpy()  
#                 for box, conf, cls in zip(boxes, confidences, classes):
#                     detections.append({
#                         'Imagen': Path(img_path).name,
#                         'Clase': model.names[int(cls)],
#                         'Confianza': float(conf),
#                         'Box_X1': float(box[0]),
#                         'Box_Y1': float(box[1]),
#                         'Box_X2': float(box[2]),
#                         'Box_Y2': float(box[3])
#                     })
#         return detections


#----------------------------------------------New-----------------------------------------------------------

class Controller(object):
    def __init__(self):
        print("Load controller... test")

    def adjust_label_position(self, img, box, label, conf, margin=10):
        """
        Ajusta la posición de la etiqueta para evitar que se salga de la imagen.
        
        Args:
            img: Imagen en formato numpy array
            box: Coordenadas del bounding box [x1, y1, x2, y2]
            label: Texto de la etiqueta
            conf: Valor de confianza
            margin: Margen desde el borde de la imagen
        
        Returns:
            tuple: Posición ajustada (x, y) para la etiqueta
        """
        img_height, img_width = img.shape[:2]
        
        # Calcula el tamaño aproximado del texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        text = f'{label} {conf:.2f}'
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Posición base (esquina superior izquierda del box)
        x = box[0]
        y = box[1] - 10  # 10 píxeles arriba del box
        
        # Ajuste horizontal si la etiqueta se sale por la derecha
        if x + text_width > img_width - margin:
            x = img_width - text_width - margin
        
        # Ajuste vertical si la etiqueta se sale por arriba
        if y - text_height < margin:
            y = box[1] + text_height + margin
        
        return int(x), int(y)

    def plot_detections(self, img, predictions, font_size=12, line_width=3):
        """
        Draws detections with adjusted labels

        Args:
            img: original image.
            predictions: YOLO model predictions
            font_size: Font size
            line_width: Width of the bounding box lines
            
        Returns:
            numpy.ndarray: Image with drawn detections.
        """
        output_img = img.copy()
        
        for pred in predictions:
            boxes = pred.boxes.xyxy.cpu().numpy()
            confs = pred.boxes.conf.cpu().numpy()
            cls = pred.boxes.cls.cpu().numpy()
            
            for box, conf, cl in zip(boxes, confs, cls):
                # Dibuja el bounding box
                cv2.rectangle(output_img, 
                            (int(box[0]), int(box[1])), 
                            (int(box[2]), int(box[3])), 
                            (0, 255, 0), 
                            line_width)
                
                # Obtiene la etiqueta
                label = pred.names[int(cl)]
                
                # Ajusta la posición de la etiqueta
                x, y = self.adjust_label_position(output_img, box, label, conf)
                
                # Dibuja el fondo de la etiqueta
                text = f'{label} {conf:.2f}'
                (text_width, text_height), _ = cv2.getTextSize(text, 
                                                             cv2.FONT_HERSHEY_SIMPLEX, 
                                                             0.5, 1)
                cv2.rectangle(output_img, 
                            (x, y - text_height), 
                            (x + text_width, y + 5), 
                            (0, 255, 0), 
                            -1)
                
                # Dibuja el texto
                cv2.putText(output_img, 
                          text, 
                          (x, y), 
                          cv2.FONT_HERSHEY_SIMPLEX, 
                          0.5, 
                          (0, 0, 0), 
                          1)
        
        return output_img

    def detectar_objetos(self, model, image_paths):
        """
        Detect objects in the given images using the specified model.

        Args:
            model: The object detection model to use for predictions.
            image_paths (list): List of paths to the images to process.

        Returns:
            list: A list of dictionaries containing detection details.
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

    def upload_images(self, model_path, files: List[UploadFile]):
        """
        Upload and process images using a YOLO model with improved label positioning.
        
        Args:
            model_path: Path to the YOLO model file
            files: List of images to upload and process
            
        Returns:
            JSONResponse: Processed image data with detections
        """
        try:
            upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')  # Valor por defecto 'uploads' si no está definido
            os.makedirs(upload_folder, exist_ok=True)
            processed_images = []
            detections = []

            for file in files:
                file_path = os.path.join(upload_folder, file.filename)

                # Guardar archivo subido
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                print(f"Uploaded image: {file.filename}")

                # Cargar modelo y procesar imagen
                model = YOLO(model_path)
                img = cv2.imread(file_path)
                if img is None:
                    raise HTTPException(status_code=400, 
                                     detail=f"Failed to read image: {file.filename}")

                # Realizar predicciones y dibujar resultados
                predictions = model.predict(img)
                output_img = self.plot_detections(img, predictions)
                
                # Codificar imagen resultante
                retval, buffer = cv2.imencode('.jpg', output_img)
                if not retval:
                    raise HTTPException(status_code=500, 
                                     detail=f"Failed to encode image: {file.filename}")

                print(f"Image {file.filename} processed and encoded successfully")
                encoded_img = base64.b64encode(buffer).decode('utf-8')
                
                # Obtener detecciones y preparar respuesta
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

                # Limpieza: eliminar archivo temporal
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Archivo temporal {file_path} eliminado con éxito.")
                    
            return JSONResponse(content=processed_images)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, 
                             detail=f"An error occurred: {str(e)}")