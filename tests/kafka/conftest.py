import pytest
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from ..src.persistent_sensor_storage.kafka.config import get_kafka_config, TOPICS


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def kafka_config():
    """Get Kafka configuration for testing."""
    config = get_kafka_config()
    # Override any config values specific to testing if needed
    return config


@pytest.fixture(scope="session")
async def test_producer(kafka_config):
    """Create a test producer instance."""
    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_config['bootstrap.servers'],
        client_id='test-producer'
    )
    await producer.start()
    yield producer
    await producer.stop()


@pytest.fixture(scope="session")
async def test_consumer(kafka_config):
    """Create a test consumer instance."""
    consumer = AIOKafkaConsumer(
        *TOPICS.values(),  # Subscribe to all topics
        bootstrap_servers=kafka_config['bootstrap.servers'],
        group_id='test-consumer-group',
        auto_offset_reset='earliest'
    )
    await consumer.start()
    yield consumer
    await consumer.stop()


@pytest.fixture(scope="function")
async def clear_topics(test_producer, test_consumer):
    """Clear all messages from topics before each test."""
    # Reset consumer offsets to the beginning
    await test_consumer.seek_to_beginning()
    # Consume all existing messages
    while True:
        try:
            messages = await test_consumer.getmany(timeout_ms=1000)
            if not messages:
                break
        except Exception:
            break
    yield
