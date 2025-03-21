import json
from typing import Any
from confluent_kafka import Producer
from .config import get_kafka_config, TOPICS
from .schemas import NodeEvent, SensorEvent, SensorReading


class KafkaProducer:
    def __init__(self):
        self.producer = Producer(get_kafka_config())

    def _delivery_report(self, err: Any, msg: Any) -> None:
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def produce_event(self, topic: str, event: NodeEvent | SensorEvent | SensorReading) -> None:
        """Produce an event to a Kafka topic."""
        try:
            self.producer.produce(
                topic,
                key=str(event.sensor_id if hasattr(event, 'sensor_id') else event.node_id),
                value=event.json(),
                callback=self._delivery_report
            )
            self.producer.poll(0)  # Trigger delivery reports
        except Exception as e:
            print(f'Failed to produce message: {e}')

    def produce_node_event(self, event: NodeEvent) -> None:
        """Produce a node event."""
        self.produce_event(TOPICS['node_events'], event)

    def produce_sensor_event(self, event: SensorEvent) -> None:
        """Produce a sensor event."""
        self.produce_event(TOPICS['sensor_events'], event)

    def produce_sensor_reading(self, reading: SensorReading) -> None:
        """Produce a sensor reading."""
        self.produce_event(TOPICS['sensor_readings'], reading)

    def close(self) -> None:
        """Flush and close the producer."""
        self.producer.flush()


# Global producer instance
producer = KafkaProducer() 