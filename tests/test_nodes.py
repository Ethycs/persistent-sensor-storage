from fastapi.testclient import TestClient
from src.persistent_sensor_storage.main import app
import os

# Use the API_BASE_URL environment variable if set, otherwise use the default
base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
client = TestClient(app, base_url=base_url)


def test_create_and_get_node():
    # Create a new node
    response = client.post(
        "/nodes", json={"serial_number": "SN123", "name": "Test Node"})
    assert response.status_code == 201
    node = response.json()
    node_id = node["id"]

    # Retrieve the created node
    response = client.get(f"/nodes/{node_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "SN123"
    assert data["name"] == "Test Node"


def test_list_nodes():
    # Test GET /nodes/
    response = client.get("/nodes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_node_by_serial():
    # Test GET /nodes/?serial_number=SN123
    response = client.get("/nodes/?serial_number=SN123")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["serial_number"] == "SN123"


def test_attach_sensor_to_node():
    # Test POST /nodes/{node_id}/sensors
    # First create a node and sensor
    node_response = client.post("/nodes", json={"serial_number": "SN456", "name": "Test Node"})
    node_id = node_response.json()["id"]
    
    sensor_response = client.post("/sensors", json={"serial_number": "SENSOR002", "type": "temperature"})
    sensor_id = sensor_response.json()["id"]
    
    # Then attach them
    response = client.post(f"/nodes/{node_id}/sensors", params={"sensor_id": sensor_id})
    assert response.status_code == 200
    data = response.json()
    assert data["node_id"] == node_id
