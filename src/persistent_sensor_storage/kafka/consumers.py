import json
import asyncio
from typing import Callable, Dict, Any
from aiokafka import AIOKafkaConsumer
from .config import get_kafka_config, TOPICS
from .schemas import NodeEvent, SensorEvent, SensorReading


class KafkaConsumer:
    def __init__(self, topic: str, group_id: str):
        config = get_kafka_config()
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=config['bootstrap.servers'],
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        self.handlers: Dict[str, Callable] = {}

    def register_handler(self, event_type: str, handler: Callable) -> None:
        """Register a handler for a specific event type."""
        self.handlers[event_type] = handler

    async def start(self) -> None:
        """Start the consumer."""
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    value = json.loads(msg.value)
                    event_type = value.get('event_type')
                    if event_type in self.handlers:
                        await self.handlers[event_type](value)
                except json.JSONDecodeError:
                    print(f"Failed to decode message: {msg.value}")
                except Exception as e:
                    print(f"Error processing message: {e}")
        finally:
            await self.consumer.stop()

    async def stop(self) -> None:
        """Stop the consumer."""
        await self.consumer.stop()


# Example handlers
async def handle_node_created(event: Dict[str, Any]) -> None:
    """Handle node created events."""
    print(f"Node created: {event}")

async def handle_sensor_created(event: Dict[str, Any]) -> None:
    """Handle sensor created events."""
    print(f"Sensor created: {event}")

async def handle_sensor_attached(event: Dict[str, Any]) -> None:
    """Handle sensor attached events."""
    print(f"Sensor attached: {event}")

# Create consumers for each topic
node_consumer = KafkaConsumer(TOPICS['node_events'], 'node-events-group')
sensor_consumer = KafkaConsumer(TOPICS['sensor_events'], 'sensor-events-group')
readings_consumer = KafkaConsumer(TOPICS['sensor_readings'], 'sensor-readings-group')

# Register handlers
node_consumer.register_handler('created', handle_node_created)
sensor_consumer.register_handler('created', handle_sensor_created)
sensor_consumer.register_handler('attached', handle_sensor_attached) 