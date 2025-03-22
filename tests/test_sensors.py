import pytest


@pytest.mark.integration
def test_create_and_get_sensor(client):
    # Create a new sensor
    response = client.post(
        "/sensors",
        json={
            "serial_number": "SENSOR001",
            "manufacturer": "Test Mfg",
            "model": "TempSensor",
            "modality": "temperature"
        })
    assert response.status_code == 201
    sensor = response.json()
    assert isinstance(sensor["id"], str)
    sensor_id = sensor["id"]

    # Retrieve the created sensor
    response = client.get(f"/sensors/{sensor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "SENSOR001"
    assert data["manufacturer"] == "Test Mfg"
    assert data["model"] == "TempSensor"
    assert data["modality"] == "temperature"
    assert isinstance(data["id"], str)
    if data["node_id"]:
        assert isinstance(data["node_id"], str)


@pytest.mark.integration
def test_list_sensors(client):
    # Test GET /sensors/
    response = client.get("/sensors/")
    assert response.status_code == 200
    sensors = response.json()
    assert isinstance(sensors, list)
    if sensors:
        assert isinstance(sensors[0]["id"], str)
        if sensors[0]["node_id"]:
            assert isinstance(sensors[0]["node_id"], str)


@pytest.mark.integration
def test_get_sensor_by_manufacturer(client):
    # First create a sensor
    response = client.post(
        "/sensors",
        json={
            "serial_number": "SENSOR002",
            "manufacturer": "Test Mfg",
            "model": "TempSensor",
            "modality": "temperature"
        })
    assert response.status_code == 201

    # Test GET /sensors/?manufacturer=Test Mfg
    response = client.get("/sensors/?manufacturer=Test Mfg")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["manufacturer"] == "Test Mfg"
    assert isinstance(data[0]["id"], str)


@pytest.mark.integration
def test_get_sensor_by_model(client):
    # Create test sensor first
    create_response = client.post(
        "/sensors",
        json={
            "serial_number": "TEST123",
            "manufacturer": "Test Mfg",
            "model": "TempSensor",
            "modality": "temperature"
        })
    assert create_response.status_code == 201
    
    # Test GET /sensors/?model=TempSensor
    response = client.get("/sensors/?model=TempSensor")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["model"] == "TempSensor"
    assert isinstance(data[0]["id"], str)


@pytest.mark.integration
def test_get_sensor_by_modality(client):
    # Create test sensor first
    create_response = client.post(
        "/sensors",
        json={
            "serial_number": "TEST456",
            "manufacturer": "Test Mfg",
            "model": "TempSensor",
            "modality": "temperature"
        })
    assert create_response.status_code == 201
    
    # Test GET /sensors/?modality=temperature
    response = client.get("/sensors/?modality=temperature")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["modality"] == "temperature"
    assert isinstance(data[0]["id"], str)


@pytest.mark.integration
def test_update_sensor(client):
    # Create a sensor first
    response = client.post(
        "/sensors",
        json={
            "serial_number": "SENSOR003",
            "manufacturer": "Old Mfg",
            "model": "OldModel",
            "modality": "humidity"
        })
    assert response.status_code == 201
    sensor_id = response.json()["id"]
    assert isinstance(sensor_id, str)

    # Update the sensor
    response = client.put(
        f"/sensors/{sensor_id}",
        json={
            "manufacturer": "New Mfg",
            "model": "NewModel",
            "modality": "temperature"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["manufacturer"] == "New Mfg"
    assert data["model"] == "NewModel"
    assert data["modality"] == "temperature"
    assert isinstance(data["id"], str)


@pytest.mark.integration
def test_sensor_update_optional_fields(client):
    # Create a sensor
    response = client.post(
        "/sensors",
        json={
            "serial_number": "SENSOR004",
            "manufacturer": "Test Mfg",
            "model": "TestModel",
            "modality": "temperature"
        })
    assert response.status_code == 201
    sensor_id = response.json()["id"]

    # Test partial update
    response = client.patch(
        f"/sensors/{sensor_id}",
        json={"manufacturer": "Updated Mfg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["manufacturer"] == "Updated Mfg"
    assert data["model"] == "TestModel"  # Unchanged
    assert data["modality"] == "temperature"  # Unchanged


@pytest.mark.integration
def test_sensor_id_format(client):
    # Test invalid sensor ID format
    # response = client.get("/sensors/invalid-id")
    # assert response.status_code == 422  # Validation error

    # Test non-existent but valid format sensor ID
    response = client.get("/sensors/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404  # Not found error


@pytest.mark.integration
def test_sensor_node_relationship(client):
    # Create a node
    node_response = client.post(
        "/nodes",
        json={
            "serial_number": "NODE001",
            "firmware_version": "1.0.0"
        })
    assert node_response.status_code == 201
    node_id = node_response.json()["id"]

    # Create a sensor
    sensor_response = client.post(
        "/sensors",
        json={
            "serial_number": "SENSOR005",
            "manufacturer": "Test Mfg",
            "model": "TestModel",
            "modality": "temperature"
        })
    assert sensor_response.status_code == 201
    sensor_id = sensor_response.json()["id"]

    # Attach sensor to node
    response = client.post(
        f"/nodes/{node_id}/sensors",
        json={"sensor_id": sensor_id}
    )
    assert response.status_code == 200

    # Verify sensor shows up in node's sensor list
    node_response = client.get(f"/nodes/{node_id}/full")
    assert node_response.status_code == 200
    node_data = node_response.json()
    assert any(s["id"] == sensor_id for s in node_data["sensors"])

    # Verify node_id in sensor response
    sensor_response = client.get(f"/sensors/{sensor_id}")
    assert sensor_response.status_code == 200
    sensor_data = sensor_response.json()
    assert sensor_data["node_id"] == node_id
