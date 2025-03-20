from fastapi.testclient import TestClient
from src.persistent_sensor_storage.main import app
import os

# Use the API_BASE_URL environment variable if set, otherwise use the default
base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
client = TestClient(app, base_url=base_url)


def test_create_and_get_sensor():
    # Create a new sensor
    response = client.post(
        "/sensors", json={"serial_number": "SENSOR001", "type": "temperature"})
    assert response.status_code == 201
    sensor = response.json()
    sensor_id = sensor["id"]

    # Retrieve the created sensor
    response = client.get(f"/sensors/{sensor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "SENSOR001"
    assert data["type"] == "temperature"


def test_list_sensors():
    # Test GET /sensors/
    response = client.get("/sensors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_sensor_by_serial():
    # Test GET /sensors/?serial_number=SENSOR001
    response = client.get("/sensors/?serial_number=SENSOR001")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["serial_number"] == "SENSOR001"
