from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class EventType(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    ATTACHED = "attached"
    DETACHED = "detached"


class NodeEvent(BaseModel):
    event_type: EventType
    node_id: int
    serial_number: str
    name: Optional[str]
    timestamp: datetime = datetime.utcnow()


class SensorEvent(BaseModel):
    event_type: EventType
    sensor_id: int
    serial_number: str
    type: str
    node_id: Optional[int]
    timestamp: datetime = datetime.utcnow()


class SensorReading(BaseModel):
    sensor_id: int
    node_id: Optional[int]
    reading_type: str
    value: float
    unit: str
    timestamp: datetime = datetime.utcnow() 