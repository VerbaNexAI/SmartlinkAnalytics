import datetime
import os
import shutil
import cv2
from fastapi import HTTPException, UploadFile
from starlette.responses import JSONResponse
from ultralytics import YOLO
from pathlib import Path

def detectar_objetos(model, image_paths):
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

def upload_images(model_path, files):
    """
    Upload and process images using a YOLO model.
    :param files: List of images to upload.
    :type files: List[UploadFile]
    :return: JSON response with processed image data.
    :rtype: JSONResponse
    :raises HTTPException: If there is an error during image upload or processing.
    """
    try:
        # Set default upload folder if not specified
        upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
        processed_folder = os.getenv('PROCESSED_FOLDER', 'processed_images')
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(processed_folder, exist_ok=True)

        processed_images = []

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
            detections = []

            for result in predictions:
                # Access the boxes attribute to get detected objects
                for box in result.boxes:
                    # Convert the confidence score tensor to a float
                    conf = box.conf.item()
                    # Convert confidence to percentage and round it
                    conf_percentage = round(conf * 100, 2)
                    cls = int(box.cls.item())

                    # Extract bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    label = f"{model.names[cls]}: {conf_percentage}%"

                    # Draw rectangle and label on the image
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Append detection details to list
                    detections.append({
                        "class": model.names[cls],
                        "confidence": conf_percentage,
                        "Box_X1": x1,
                        "Box_Y1": y1,
                        "Box_X2": x2,
                        "Box_Y2": y2
                    })

            # Save processed image
            processed_image_path = os.path.join(processed_folder, file.filename)
            retval = cv2.imwrite(processed_image_path, img)
            if not retval:
                raise HTTPException(status_code=500, detail=f"Failed to save processed image: {file.filename}")

            print(f"Image {file.filename} processed and saved successfully")

            fecha_generacion = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nombre_empresa = 'SERINGTEC'

            processed_images.append({
                "filename": file.filename,
                "image_path": processed_image_path,  # Path to the saved image
                "Fecha de Generación": fecha_generacion,
                "Empresa": nombre_empresa,
                "Detecciones": detections
            })

        return JSONResponse(content=processed_images)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Example usage
model_path = r'C:\IA\SmartlinkAnalytics-web\SmartlinkAnalytics\Backend\config\data\models\mec-s3d-v1.pt'
files = [
    UploadFile(filename="0_CSE02095METPLM000001_PlanimetriaGeneralTuberiaCASE_0095_AFC2-COM LRC 21.03.24-1.jpg", file=open(r"C:\IA\SmartlinkAnalytics-web\SmartlinkAnalytics\Backend\test\0_CSE02095METPLM000001_PlanimetriaGeneralTuberiaCASE_0095_AFC2-COM LRC 21.03.24-1.jpg", "rb"))
]
response = upload_images(model_path, files)
print(response)
