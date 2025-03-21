import pytest


@pytest.mark.integration
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


@pytest.mark.integration
def test_nonexistent_endpoint(client):
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404


@pytest.mark.integration
def test_invalid_node_input(client):
    # Test where required firmware_version is missing
    response = client.post(
        "/nodes", json={"serial_number": "TEST123"})
    assert response.status_code == 422
    assert response.json()["detail"] == "Firmware version is required"

    # Test where integer is used instead of string
    response = client.post(
        "/nodes", json={"serial_number": 123, "firmware_version": "1.0.0"})
    assert response.status_code == 422


@pytest.mark.integration
def test_invalid_sensor_input(client):
    # Test where required fields are missing
    response = client.post(
        "/sensors", json={"serial_number": "TEST123"})
    assert response.status_code == 422
    assert response.json()["detail"] == (
        "Manufacturer, model, and modality are required"
    )

    # Test where integer is used instead of string
    response = client.post(
        "/sensors",
        json={
            "serial_number": 123,
            "manufacturer": "Test Mfg",
            "model": "Model1",
            "modality": "temperature"
        })
    assert response.status_code == 422


@pytest.mark.integration
def test_node_not_found(client):
    # Test where a non-existent node ID is used
    response = client.get("/nodes/999999")  # Non-existent node ID
    assert response.status_code == 404  # Expecting a 404 Not Found error


@pytest.mark.integration
def test_attach_sensor_to_node_error(client):
    # Test POST /nodes/{node_id}/sensors with incorrect parameters
    # Using string instead of integer for sensor_id
    response = client.post("/nodes/1/sensors", json={"sensor_id": "1"})
    # Expecting a validation error due to the incorrect parameter type
    assert response.status_code == 422
