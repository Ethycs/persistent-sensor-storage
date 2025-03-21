import pytest


@pytest.mark.integration
def test_create_and_get_node(client):
    # Create a new node
    response = client.post(
        "/nodes", json={
            ""
            "serial_number": "SN123",
            "firmware_version": "1.0.0"
        })
    assert response.status_code == 201
    node = response.json()
    assert isinstance(node["id"], str)
    node_id = node["id"]

    # Retrieve the created node
    response = client.get(f"/nodes/{node_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "SN123"
    assert data["firmware_version"] == "1.0.0"
    assert isinstance(data["id"], str)


@pytest.mark.integration
def test_list_nodes(client):
    # Test GET /nodes/
    response = client.get("/nodes/")
    assert response.status_code == 200
    nodes = response.json()
    assert isinstance(nodes, list)
    if nodes:
        assert isinstance(nodes[0]["id"], str)


@pytest.mark.integration
def test_get_node_by_serial(client):
    # First create a node
    response = client.post(
        "/nodes", json={
            "serial_number": "SN123",
            "firmware_version": "1.0.0"
        })
    assert response.status_code == 201

    # Test GET /nodes/?serial_number=SN123
    response = client.get("/nodes/?serial_number=SN123")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["serial_number"] == "SN123"
    assert isinstance(data[0]["id"], str)


@pytest.mark.integration
def test_get_node_with_sensors(client):
    # Create a node
    node_response = client.post(
        "/nodes", json={
            "serial_number": "SN456",
            "firmware_version": "1.0.0"
        })
    assert node_response.status_code == 201
    node_id = node_response.json()["id"]
    
    # Create a sensor
    sensor_response = client.post(
        "/sensors", 
        json={
            "serial_number": "SENSOR002",
            "manufacturer": "Test Mfg",
            "model": "TempSensor",
            "modality": "temperature"
        })
    assert sensor_response.status_code == 201
    sensor_id = sensor_response.json()["id"]
    
    # Attach sensor to node
    attach_response = client.post(
        f"/nodes/{node_id}/sensors",
        json={"sensor_id": sensor_id}
    )
    assert attach_response.status_code == 200
    
    # Get node with full sensor details
    response = client.get(f"/nodes/{node_id}/full")
    assert response.status_code == 200
    data = response.json()
    assert "sensors" in data
    assert isinstance(data["sensors"], list)
    assert len(data["sensors"]) > 0
    assert isinstance(data["sensors"][0]["id"], str)


@pytest.mark.integration
def test_attach_sensor_to_node(client):
    # Create a node
    node_response = client.post(
        "/nodes", json={
            "serial_number": "SN789",
            "firmware_version": "1.0.0"
        })
    assert node_response.status_code == 201
    node_id = node_response.json()["id"]
    assert isinstance(node_id, str)
    
    # Create a sensor
    sensor_response = client.post(
        "/sensors", 
        json={
            "serial_number": "SENSOR003",
            "manufacturer": "Test Mfg",
            "model": "TempSensor",
            "modality": "temperature"
        })
    assert sensor_response.status_code == 201
    sensor_id = sensor_response.json()["id"]
    assert isinstance(sensor_id, str)
    
    # Attach them
    response = client.post(
        f"/nodes/{node_id}/sensors",
        json={"sensor_id": sensor_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["node_id"], str)
    assert data["node_id"] == node_id


@pytest.mark.integration
def test_node_id_format(client):
    # Test invalid node ID format
    # There are no invalid node IDs in the current implementation
    # response = client.get("/nodes/invalid-id")
    # assert response.status_code == 422  # Validation error

    # Test non-existent but valid format node ID
    response = client.get("/nodes/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404  # Not found error


@pytest.mark.integration
def test_node_update_optional_fields(client):
    # Create a node
    response = client.post(
        "/nodes", json={
            "serial_number": "SN101",
            "firmware_version": "1.0.0"
        })
    assert response.status_code == 201
    node_id = response.json()["id"]
    
    # Test partial update
    response = client.patch(
        f"/nodes/{node_id}",
        json={"firmware_version": "2.0.0"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["firmware_version"] == "2.0.0"
    assert data["serial_number"] == "SN101"  # Unchanged
