import pytest
import asyncio
from datetime import datetime
from src.persistent_sensor_storage.kafka.schemas import (
    NodeEvent, SensorEvent, SensorReading, EventType
)
from src.persistent_sensor_storage.kafka.consumers import KafkaConsumer
from src.persistent_sensor_storage.kafka.config import TOPICS


@pytest.mark.asyncio
async def test_node_lifecycle(test_producer, clear_topics):
    """Test complete node lifecycle with events."""
    # Setup test data
    node_id = 1
    serial_number = "TEST-NODE-001"
    
    # Track events
    received_events = []
    
    # Setup consumer
    async def event_handler(event_data):
        received_events.append(event_data)
    
    consumer = KafkaConsumer(TOPICS['node_events'], 'test-group')
    for event_type in EventType:
        consumer.register_handler(event_type, event_handler)
    
    # Start consumer
    consumer_task = asyncio.create_task(consumer.start())
    
    # Create node event
    create_event = NodeEvent(
        event_type=EventType.CREATED,
        node_id=node_id,
        serial_number=serial_number,
        name="Test Node",
        timestamp=datetime.utcnow()
    )
    await test_producer.send_and_wait(
        TOPICS['node_events'],
        create_event.json().encode()
    )
    
    # Update node event
    update_event = NodeEvent(
        event_type=EventType.UPDATED,
        node_id=node_id,
        serial_number=serial_number,
        name="Updated Test Node",
        timestamp=datetime.utcnow()
    )
    await test_producer.send_and_wait(
        TOPICS['node_events'],
        update_event.json().encode()
    )
    
    # Delete node event
    delete_event = NodeEvent(
        event_type=EventType.DELETED,
        node_id=node_id,
        serial_number=serial_number,
        name=None,
        timestamp=datetime.utcnow()
    )
    await test_producer.send_and_wait(
        TOPICS['node_events'],
        delete_event.json().encode()
    )
    
    # Wait for events to be processed
    await asyncio.sleep(2)
    
    # Stop consumer
    await consumer.stop()
    consumer_task.cancel()
    
    # Verify all lifecycle events were processed
    assert len(received_events) == 3
    events_by_type = {e['event_type']: e for e in received_events}
    
    assert EventType.CREATED in events_by_type
    assert events_by_type[EventType.CREATED]['name'] == "Test Node"
    
    assert EventType.UPDATED in events_by_type
    assert events_by_type[EventType.UPDATED]['name'] == "Updated Test Node"
    
    assert EventType.DELETED in events_by_type


@pytest.mark.asyncio
async def test_sensor_with_readings(test_producer, clear_topics):
    """Test sensor events with readings."""
    # Setup test data
    sensor_id = 1
    node_id = 1
    serial_number = "TEST-SENSOR-001"
    
    # Track events and readings
    received_events = []
    received_readings = []
    
    # Setup consumers
    async def event_handler(event_data):
        received_events.append(event_data)
    
    async def reading_handler(reading_data):
        received_readings.append(reading_data)
    
    event_consumer = KafkaConsumer(
        TOPICS['sensor_events'],
        'test-events-group'
    )
    reading_consumer = KafkaConsumer(
        TOPICS['sensor_readings'],
        'test-readings-group'
    )
    
    for event_type in EventType:
        event_consumer.register_handler(event_type, event_handler)
    reading_consumer.register_handler('reading', reading_handler)
    
    # Start consumers
    event_task = asyncio.create_task(event_consumer.start())
    reading_task = asyncio.create_task(reading_consumer.start())
    
    # Create sensor
    create_event = SensorEvent(
        event_type=EventType.CREATED,
        sensor_id=sensor_id,
        serial_number=serial_number,
        type="temperature",
        node_id=None,
        timestamp=datetime.utcnow()
    )
    await test_producer.send_and_wait(
        TOPICS['sensor_events'],
        create_event.json().encode()
    )
    
    # Attach sensor to node
    attach_event = SensorEvent(
        event_type=EventType.ATTACHED,
        sensor_id=sensor_id,
        serial_number=serial_number,
        type="temperature",
        node_id=node_id,
        timestamp=datetime.utcnow()
    )
    await test_producer.send_and_wait(
        TOPICS['sensor_events'],
        attach_event.json().encode()
    )
    
    # Send readings
    for temp in [20.5, 21.0, 21.5]:
        reading = SensorReading(
            sensor_id=sensor_id,
            node_id=node_id,
            reading_type="temperature",
            value=temp,
            unit="celsius",
            timestamp=datetime.utcnow()
        )
        await test_producer.send_and_wait(
            TOPICS['sensor_readings'],
            reading.json().encode()
        )
    
    # Wait for events to be processed
    await asyncio.sleep(2)
    
    # Stop consumers
    await event_consumer.stop()
    await reading_consumer.stop()
    event_task.cancel()
    reading_task.cancel()
    
    # Verify events
    assert len(received_events) == 2
    events_by_type = {e['event_type']: e for e in received_events}
    
    assert EventType.CREATED in events_by_type
    assert events_by_type[EventType.CREATED]['node_id'] is None
    
    assert EventType.ATTACHED in events_by_type
    assert events_by_type[EventType.ATTACHED]['node_id'] == node_id
    
    # Verify readings
    assert len(received_readings) == 3
    readings = sorted(r['value'] for r in received_readings)
    assert readings == [20.5, 21.0, 21.5]
