from fastapi.testclient import TestClient
from src.persistent_sensor_storage.main import app

client = TestClient(app)

def test_create_and_get_sensor():
    # Create a new sensor
    response = client.post("/sensors", json={"serial_number": "SENSOR001", "type": "temperature"})
    assert response.status_code == 201
    sensor = response.json()
    sensor_id = sensor["id"]

    # Retrieve the created sensor
    response = client.get(f"/sensors/{sensor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "SENSOR001"
    assert data["type"] == "temperature"
