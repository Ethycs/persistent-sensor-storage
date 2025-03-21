from pydantic import BaseModel
from typing import Optional, List

# --- Sensor Schemas ---


class SensorBase(BaseModel):
    serial_number: str
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
    sensor_id: int


class Sensor(SensorBase):
    id: int
    node_id: Optional[int]

    class Config:
        orm_mode = True

# --- Node Schemas ---


class NodeBase(BaseModel):
    serial_number: str
    firmware_version: str


class NodeCreate(NodeBase):
    pass


class NodeUpdate(BaseModel):
    serial_number: Optional[str] = None
    firmware_version: Optional[str] = None


class NodeBasic(NodeBase):
    id: int

    class Config:
        orm_mode = True


class Node(NodeBasic):
    sensors: List[Sensor] = []   # List of attached sensors
