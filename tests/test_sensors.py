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
    sensor_id = sensor["id"]

    # Retrieve the created sensor
    response = client.get(f"/sensors/{sensor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["serial_number"] == "SENSOR001"
    assert data["manufacturer"] == "Test Mfg"
    assert data["model"] == "TempSensor"
    assert data["modality"] == "temperature"


@pytest.mark.integration
def test_list_sensors(client):
    # Test GET /sensors/
    response = client.get("/sensors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.integration
def test_get_sensor_by_manufacturer(client):
    # Test GET /sensors/?manufacturer=Test Mfg
    response = client.get("/sensors/?manufacturer=Test Mfg")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["manufacturer"] == "Test Mfg"


@pytest.mark.integration
def test_get_sensor_by_model(client):
    # Test GET /sensors/?model=TempSensor
    response = client.get("/sensors/?model=TempSensor")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["model"] == "TempSensor"


@pytest.mark.integration
def test_get_sensor_by_modality(client):
    # Test GET /sensors/?modality=temperature
    response = client.get("/sensors/?modality=temperature")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["modality"] == "temperature"


@pytest.mark.integration
def test_update_sensor(client):
    # Create a sensor first
    response = client.post(
        "/sensors",
        json={
            "serial_number": "SENSOR002",
            "manufacturer": "Old Mfg",
            "model": "OldModel",
            "modality": "humidity"
        })
    sensor_id = response.json()["id"]

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
