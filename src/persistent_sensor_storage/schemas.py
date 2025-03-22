from pydantic import BaseModel
from typing import Optional, List

# --- Sensor Schemas ---


class SensorBase(BaseModel):
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


class Sensor(SensorBase):
    id: str
    node_id: Optional[str]

    class Config:
        orm_mode = True

# --- Node Schemas ---


class NodeBase(BaseModel):
    serial_number: Optional[str] = None
    firmware_version: str


class NodeCreate(NodeBase):
    pass


class NodeUpdate(BaseModel):
    serial_number: Optional[str] = None
    firmware_version: Optional[str] = None


class NodeBasic(NodeBase):
    id: str

    class Config:
        orm_mode = True


class Node(NodeBasic):
    sensors: List[Sensor] = []   # List of attached sensors
