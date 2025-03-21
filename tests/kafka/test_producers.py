import pytest
import json
from datetime import datetime
from src.persistent_sensor_storage.kafka.schemas import (
    NodeEvent, SensorEvent, SensorReading, EventType
)
from src.persistent_sensor_storage.kafka.producers import KafkaProducer
from src.persistent_sensor_storage.kafka.config import TOPICS


@pytest.mark.asyncio
async def test_produce_node_event(test_consumer, clear_topics):
    """Test producing a node event."""
    producer = KafkaProducer()
    
    # Create test event
    event = NodeEvent(
        event_type=EventType.CREATED,
        node_id=1,
        serial_number="TEST-NODE-001",
        name="Test Node",
        timestamp=datetime.utcnow()
    )
    
    # Produce event
    producer.produce_node_event(event)
    producer.producer.flush()
    
    # Verify message in topic
    async for msg in test_consumer:
        if msg.topic == TOPICS['node_events']:
            data = json.loads(msg.value)
            assert data['event_type'] == EventType.CREATED
            assert data['node_id'] == 1
            assert data['serial_number'] == "TEST-NODE-001"
            assert data['name'] == "Test Node"
            break


@pytest.mark.asyncio
async def test_produce_sensor_event(test_consumer, clear_topics):
    """Test producing a sensor event."""
    producer = KafkaProducer()
    
    # Create test event
    event = SensorEvent(
        event_type=EventType.CREATED,
        sensor_id=1,
        serial_number="TEST-SENSOR-001",
        type="temperature",
        node_id=None,
        timestamp=datetime.utcnow()
    )
    
    # Produce event
    producer.produce_sensor_event(event)
    producer.producer.flush()
    
    # Verify message in topic
    async for msg in test_consumer:
        if msg.topic == TOPICS['sensor_events']:
            data = json.loads(msg.value)
            assert data['event_type'] == EventType.CREATED
            assert data['sensor_id'] == 1
            assert data['serial_number'] == "TEST-SENSOR-001"
            assert data['type'] == "temperature"
            break


@pytest.mark.asyncio
async def test_produce_sensor_reading(test_consumer, clear_topics):
    """Test producing a sensor reading."""
    producer = KafkaProducer()
    
    # Create test reading
    reading = SensorReading(
        sensor_id=1,
        node_id=1,
        reading_type="temperature",
        value=25.5,
        unit="celsius",
        timestamp=datetime.utcnow()
    )
    
    # Produce reading
    producer.produce_sensor_reading(reading)
    producer.producer.flush()
    
    # Verify message in topic
    async for msg in test_consumer:
        if msg.topic == TOPICS['sensor_readings']:
            data = json.loads(msg.value)
            assert data['sensor_id'] == 1
            assert data['node_id'] == 1
            assert data['reading_type'] == "temperature"
            assert data['value'] == 25.5
            assert data['unit'] == "celsius"
            break


@pytest.mark.asyncio
async def test_produce_multiple_events(test_consumer, clear_topics):
    """Test producing multiple events in sequence."""
    producer = KafkaProducer()
    
    # Create and produce node event
    node_event = NodeEvent(
        event_type=EventType.CREATED,
        node_id=2,
        serial_number="TEST-NODE-002",
        name="Test Node 2",
        timestamp=datetime.utcnow()
    )
    producer.produce_node_event(node_event)
    
    # Create and produce sensor event
    sensor_event = SensorEvent(
        event_type=EventType.CREATED,
        sensor_id=2,
        serial_number="TEST-SENSOR-002",
        type="humidity",
        node_id=2,
        timestamp=datetime.utcnow()
    )
    producer.produce_sensor_event(sensor_event)
    
    # Create and produce sensor reading
    reading = SensorReading(
        sensor_id=2,
        node_id=2,
        reading_type="humidity",
        value=65.0,
        unit="percent",
        timestamp=datetime.utcnow()
    )
    producer.produce_sensor_reading(reading)
    
    producer.producer.flush()
    
    # Verify all messages were produced
    received_events = []
    async for msg in test_consumer:
        data = json.loads(msg.value)
        if msg.topic == TOPICS['node_events']:
            assert data['serial_number'] == "TEST-NODE-002"
            received_events.append('node')
        elif msg.topic == TOPICS['sensor_events']:
            assert data['serial_number'] == "TEST-SENSOR-002"
            received_events.append('sensor')
        elif msg.topic == TOPICS['sensor_readings']:
            assert data['reading_type'] == "humidity"
            received_events.append('reading')
        
        if len(received_events) == 3:
            break
    
    assert set(received_events) == {'node', 'sensor', 'reading'}
