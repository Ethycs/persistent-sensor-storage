from fastapi.testclient import TestClient
from src.persistent_sensor_storage.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_error_assertion():
    # Test that intentionally causes an assertion error
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 200  # This will cause an assertion error


def test_invalid_input_type():
    # Test where an integer is used instead of a string
    response = client.post(
        "/nodes", json={"serial_number": 123, "name": "Test Node"})
    # Expecting a validation error due to the wrong input type
    assert response.status_code == 422


def test_invalid_input_length():
    # Test where a string exceeding the maximum length is used
    response = client.post(
        "/nodes", json={"serial_number": "A" * 50, "name": "Test Node"})
    # Expecting a validation error due to the serial number length exceeding the limit
    assert response.status_code == 422


def test_node_not_found():
    # Test where a non-existent node ID is used
    response = client.get("/nodes/999999")  # Non-existent node ID
    assert response.status_code == 404  # Expecting a 404 Not Found error


def test_attach_sensor_to_node_error():
    # Test POST /nodes/{node_id}/sensors with incorrect parameters
    # Using string instead of integer for sensor_id
    response = client.post("/nodes/1/sensors", json={"sensor_id": "1"})
    # Expecting a validation error due to the incorrect parameter type
    assert response.status_code == 422
