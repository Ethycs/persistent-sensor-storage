from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from uuid import uuid4

# --- Base Schema ---


class EntityBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    model_config = ConfigDict(validate_default=True)


# --- Sensor Schemas ---


class SensorBase(EntityBase):
    serial_number: Optional[str] = None
    manufacturer: str
    model: str
    modality: str


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    modality: Optional[str] = None


class SensorAttachRequest(BaseModel):
    sensor_id: str


class SensorResponse(SensorBase):
    node_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- Node Schemas ---


class NodeBase(EntityBase):
    serial_number: Optional[str] = None
    firmware_version: str


class NodeCreate(NodeBase):
    pass


class NodeUpdate(BaseModel):
    serial_number: Optional[str] = None
    firmware_version: Optional[str] = None


class NodeResponse(NodeBase):
    model_config = ConfigDict(from_attributes=True)


class Node(NodeResponse):
    sensors: List[SensorResponse] = []   # List of attached sensors
