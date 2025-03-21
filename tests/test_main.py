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
    assert "firmware_version" in response.json()["detail"].lower()

    # Test where integer is used instead of string
    response = client.post(
        "/nodes", json={
            "serial_number": 123,
            "firmware_version": "1.0.0"
        })
    assert response.status_code == 422
    assert "string" in response.json()["detail"].lower()


@pytest.mark.integration
def test_invalid_sensor_input(client):
    # Test where required fields are missing
    response = client.post(
        "/sensors", json={"serial_number": "TEST123"})
    assert response.status_code == 422
    error_detail = response.json()["detail"].lower()
    required_fields = ["manufacturer", "model", "modality"]
    assert all(field in error_detail for field in required_fields)

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
    assert "string" in response.json()["detail"].lower()


@pytest.mark.integration
def test_node_not_found(client):
    # Test where a non-existent node ID is used
    response = client.get("/nodes/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.integration
def test_attach_sensor_to_node_error(client):
    # Test with invalid sensor_id format
    response = client.post(
        "/nodes/123e4567-e89b-12d3-a456-426614174000/sensors",
        json={"sensor_id": 123}  # Should be string
    )
    assert response.status_code == 422
    assert "string" in response.json()["detail"].lower()

    # Test with non-existent node and valid sensor format
    response = client.post(
        "/nodes/123e4567-e89b-12d3-a456-426614174000/sensors",
        json={"sensor_id": "456e4567-e89b-12d3-a456-426614174000"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

