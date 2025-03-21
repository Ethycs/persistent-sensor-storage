import os
from typing import Dict

def get_kafka_config() -> Dict[str, str]:
    """Get Kafka configuration from environment variables."""
    return {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        'client.id': 'sensor-storage-service',
        'auto.offset.reset': 'earliest'
    }

# Define Kafka topics
TOPICS = {
    'node_events': 'sensor-storage.node-events',
    'sensor_events': 'sensor-storage.sensor-events',
    'sensor_readings': 'sensor-storage.sensor-readings'
} 