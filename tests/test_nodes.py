from fastapi.testclient import TestClient
from src.persistent_sensor_storage.main import app

client = TestClient(app)


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
