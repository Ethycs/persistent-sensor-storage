import pytest
import asyncio
from datetime import datetime
from src.persistent_sensor_storage.kafka.schemas import (
    NodeEvent, SensorEvent, SensorReading, EventType
)
from src.persistent_sensor_storage.kafka.consumers import KafkaConsumer
from src.persistent_sensor_storage.kafka.config import TOPICS


@pytest.mark.asyncio
async def test_node_event_consumer(test_producer, clear_topics):
    """Test consuming node events."""
    # Setup test data
    test_event = NodeEvent(
        event_type=EventType.CREATED,
        node_id=1,
        serial_number="TEST-NODE-001",
        name="Test Node",
        timestamp=datetime.utcnow()
    )
    
    # Create consumer with test handler
    received_events = []
    
    async def test_handler(event_data):
        received_events.append(event_data)
    
    consumer = KafkaConsumer(TOPICS['node_events'], 'test-group')
    consumer.register_handler(EventType.CREATED, test_handler)
    
    # Start consumer
    consumer_task = asyncio.create_task(consumer.start())
    
    # Produce test event
    await test_producer.send_and_wait(
        TOPICS['node_events'],
        test_event.json().encode()
    )
    
    # Wait for event to be consumed
    await asyncio.sleep(1)
    
    # Stop consumer
    await consumer.stop()
    consumer_task.cancel()
    
    # Verify event was received and processed
    assert len(received_events) == 1
    event = received_events[0]
    assert event['event_type'] == EventType.CREATED
    assert event['serial_number'] == "TEST-NODE-001"
    assert event['name'] == "Test Node"


@pytest.mark.asyncio
async def test_sensor_event_consumer(test_producer, clear_topics):
    """Test consuming sensor events."""
    # Setup test data
    test_event = SensorEvent(
        event_type=EventType.CREATED,
        sensor_id=1,
        serial_number="TEST-SENSOR-001",
        type="temperature",
        node_id=None,
        timestamp=datetime.utcnow()
    )
    
    # Create consumer with test handler
    received_events = []
    
    async def test_handler(event_data):
        received_events.append(event_data)
    
    consumer = KafkaConsumer(TOPICS['sensor_events'], 'test-group')
    consumer.register_handler(EventType.CREATED, test_handler)
    
    # Start consumer
    consumer_task = asyncio.create_task(consumer.start())
    
    # Produce test event
    await test_producer.send_and_wait(
        TOPICS['sensor_events'],
        test_event.json().encode()
    )
    
    # Wait for event to be consumed
    await asyncio.sleep(1)
    
    # Stop consumer
    await consumer.stop()
    consumer_task.cancel()
    
    # Verify event was received and processed
    assert len(received_events) == 1
    event = received_events[0]
    assert event['event_type'] == EventType.CREATED
    assert event['serial_number'] == "TEST-SENSOR-001"
    assert event['type'] == "temperature"


@pytest.mark.asyncio
async def test_sensor_reading_consumer(test_producer, clear_topics):
    """Test consuming sensor readings."""
    # Setup test data
    test_reading = SensorReading(
        sensor_id=1,
        node_id=1,
        reading_type="temperature",
        value=25.5,
        unit="celsius",
        timestamp=datetime.utcnow()
    )
    
    # Create consumer with test handler
    received_readings = []
    
    async def test_handler(reading_data):
        received_readings.append(reading_data)
    
    consumer = KafkaConsumer(TOPICS['sensor_readings'], 'test-group')
    consumer.register_handler('reading', test_handler)
    
    # Start consumer
    consumer_task = asyncio.create_task(consumer.start())
    
    # Produce test reading
    await test_producer.send_and_wait(
        TOPICS['sensor_readings'],
        test_reading.json().encode()
    )
    
    # Wait for reading to be consumed
    await asyncio.sleep(1)
    
    # Stop consumer
    await consumer.stop()
    consumer_task.cancel()
    
    # Verify reading was received and processed
    assert len(received_readings) == 1
    reading = received_readings[0]
    assert reading['sensor_id'] == 1
    assert reading['reading_type'] == "temperature"
    assert reading['value'] == 25.5
    assert reading['unit'] == "celsius"


@pytest.mark.asyncio
async def test_consumer_error_handling(test_producer, clear_topics):
    """Test consumer error handling with invalid messages."""
    # Create consumer with test handler
    error_count = 0
    
    async def test_handler(event_data):
        raise ValueError("Test error")
    
    consumer = KafkaConsumer(TOPICS['node_events'], 'test-group')
    consumer.register_handler(EventType.CREATED, test_handler)
    
    # Override error handling to count errors
    async def error_counter(e):
        nonlocal error_count
        error_count += 1
    
    consumer._handle_error = error_counter
    
    # Start consumer
    consumer_task = asyncio.create_task(consumer.start())
    
    # Send invalid message
    await test_producer.send_and_wait(
        TOPICS['node_events'],
        b'invalid json'
    )
    
    # Wait for message processing
    await asyncio.sleep(1)
    
    # Stop consumer
    await consumer.stop()
    consumer_task.cancel()
    
    # Verify error was handled
    assert error_count > 0
