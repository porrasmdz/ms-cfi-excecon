from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas, models
import uuid

template_cyclic_count = {"name": "Test Count"}

def test_create_cyclic_count(client: TestClient):
    response = client.post("/cyclic_counts/", json=template_cyclic_count)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Count"
    assert "id" in data

def test_read_cyclic_counts(client: TestClient):
    response = client.get("/cyclic_counts/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_cyclic_count(client: TestClient):
    response = client.post("/cyclic_counts/", json=template_cyclic_count)
    data = response.json()
    count_id = data["id"]

    update_data = {"name": "Updated Test Count"}
    response = client.put(f"/cyclic_counts/{count_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Test Count"

def test_delete_cyclic_count(client: TestClient):
    # Primero creamos un registro
    response = client.post("/cyclic_counts/", json=template_cyclic_count)
    data = response.json()
    count_id = data["id"]

    # Luego lo eliminamos
    response = client.delete(f"/cyclic_counts/{count_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == count_id

##############Count_registry
def test_create_count_registry(client, sample_data):
    response = client.post(
        "/count_registries/",
        json={
            "registry_type": "system",
            "registry_units": 100,
            "registry_cost": 5000,
            "difference_units": 5,
            "difference_cost": 250,
            "product_id": str(sample_data["product_id"]),
            "cyclic_count_id": str(sample_data["cyclic_count_id"])
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["registry_type"] == "system"
    assert data["registry_units"] == 100
    assert data["registry_cost"] == 5000
    assert data["difference_units"] == 5
    assert data["difference_cost"] == 250

def test_read_count_registries(client):
    response = client.get("/count_registries/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_count_registry(client, sample_data):
    registry_id = str(sample_data["count_registry_id"])  # Asegúrate de usar un UUID válido existente
    response = client.put(
        f"/count_registries/{registry_id}",
        json={"registry_units": 150}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["registry_units"] == 150
    
def test_delete_count_registry(client, sample_data):
    registry_id = str(sample_data["count_registry_id"])  # Asegúrate de usar un UUID válido existente
    response = client.delete(f"/count_registries/{registry_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == registry_id #Deleted id

###############activity_registry
def test_create_activity_registry(client, sample_data):
    response = client.post(
        "/activity_registries/",
        json={
            "detail": "Some detail",
            "commentary": "Some commentary",
            "user": str(uuid.uuid4()),  # Asegúrate de usar un UUID válido
            "count_registry_id": str(sample_data["alt_count_registry_id"])  # Asegúrate de usar un UUID válido
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Some detail"
    assert data["commentary"] == "Some commentary"

def test_read_activity_registries(client):
    response = client.get("/activity_registries/")
    assert response.status_code == 200
    data = response.json()
    result = schemas.PaginatedResource(**data)
    assert result is not None

def test_update_activity_registry(client, sample_data):
    activity_id = str(sample_data["activity_registry"])  # Asegúrate de usar un UUID válido existente
    response = client.put(
        f"/activity_registries/{activity_id}",
        json={"detail": "Updated detail"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Updated detail"

def test_delete_activity_registry(client, sample_data):
    activity_id = str(sample_data["activity_registry"])  # Asegúrate de usar un UUID válido existente
    response = client.delete(f"/activity_registries/{activity_id}")
    assert response.status_code == 200
    data = response.json()
