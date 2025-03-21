import pytest


@pytest.mark.integration
def test_create_and_get_node(client):
    # Create a new node
    response = client.post(
        "/nodes", json={
            "serial_number": "SN123",
            "firmware_version": "1.0.0"
        })
    assert response.status_code == 201
    node = response.json()
    node_id = node["id"]

    # Retrieve the created node
    response = client.get(f"/nodes/{node_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "SN123"
    assert data["firmware_version"] == "1.0.0"


@pytest.mark.integration
def test_list_nodes(client):
    # Test GET /nodes/
    response = client.get("/nodes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.integration
def test_get_node_by_serial(client):
    # Test GET /nodes/?serial_number=SN123
    response = client.get("/nodes/?serial_number=SN123")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["serial_number"] == "SN123"


@pytest.mark.integration
def test_attach_sensor_to_node(client):
    # Test POST /nodes/{node_id}/sensors
    # First create a node and sensor
    node_response = client.post(
        "/nodes", 
        json={
            "serial_number": "SN456",
            "firmware_version": "1.0.0"
        })
    node_id = node_response.json()["id"]
    
    sensor_response = client.post(
        "/sensors", 
        json={
            "serial_number": "SENSOR002",
            "manufacturer": "Test Mfg",
            "model": "TempSensor",
            "modality": "temperature"
        })
    sensor_id = sensor_response.json()["id"]
    
    # Then attach them
    response = client.post(
        f"/nodes/{node_id}/sensors",
        json={"sensor_id": sensor_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["node_id"] == node_id
