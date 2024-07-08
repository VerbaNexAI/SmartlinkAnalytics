import datetime
import os
import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  # Asegúrate de importar correctamente tu aplicación FastAPI
from model.sql_transactions import SQLTransactions

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_sql_transactions(mocker):
    mocker.patch.object(SQLTransactions, 'get_active_projects', return_value=[
        {"name": "Project 1"},
        {"name": "Project 2"}
    ])
    mocker.patch.object(SQLTransactions, 'get_inactive_projects_from_db', return_value=[
        {"PROYECTO": "Inactive Project 1"},
        {"PROYECTO": "Inactive Project 2"}
    ])
    mocker.patch.object(SQLTransactions, 'get_project', return_value={"name": "Project 1"})
    mocker.patch.object(SQLTransactions, 'get_view_data', return_value=[
        {"label": "LABEL_0", "other_field": "value"},
        {"label": "LABEL_1", "other_field": "value"}
    ])
    mocker.patch.object(SQLTransactions, 'create_text_label_df', return_value=[
        {"label": "LABEL_0", "descripcion": "Consistent"},
        {"label": "LABEL_1", "descripcion": "Inconsistent Property Value"}
    ])

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"projects": "Here you can find the projects or SDGs"}

def test_get_projects():
    response = client.get("/api/project")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "Project 1"},
        {"name": "Project 2"}
    ]

def test_get_inactive_projects():
    response = client.get("/api/project/inactive")
    assert response.status_code == 200
    assert response.json() == [
        {"PROYECTO": "Inactive Project 1"},
        {"PROYECTO": "Inactive Project 2"}
    ]

def test_post_project_content():
    response = client.post("/api/view", json={"projects": [{"project_id": "1"}]})
    assert response.status_code == 200
    expected_combined_result = [
        {
            "label": "LABEL_0",
            "descripcion": "Consistent",
            "other_field": "value"
        },
        {
            "label": "LABEL_1",
            "descripcion": "Inconsistent Property Value",
            "other_field": "value"
        }
    ]
    assert response.json() == expected_combined_result

@patch("os.makedirs")
@patch("shutil.copyfileobj")
@patch("cv2.imread", return_value=MagicMock())
@patch("cv2.imencode", return_value=(True, MagicMock()))
@patch("base64.b64encode", return_value=b"encoded_image")
@patch("model.sql_transactions.detectar_objetos", return_value=[{"object": "detected"}])
@patch("ultralytics.YOLO")
def test_upload_images_sel(mock_yolo, mock_detectar_objetos, mock_b64encode, mock_imencode, mock_imread, mock_copyfileobj, mock_makedirs):
    files = [("files", ("test_image.jpg", io.BytesIO(b"fake_image_data"), "image/jpeg"))]
    response = client.post("/upload-image-sel", files=files)
    assert response.status_code == 200
    assert response.json() == [{
        "filename": "test_image.jpg",
        "image_base64": "encoded_image",
        "Fecha de Generación": pytest.approx(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rel=1),
        "Empresa": "SERINGTEC",
        "Detecciones": [{"object": "detected"}]
    }]

# Agrega pruebas similares para las otras rutas de carga de imágenes si es necesario
