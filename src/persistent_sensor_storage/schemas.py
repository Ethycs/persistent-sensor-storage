from pydantic import BaseModel
from typing import Optional, List

# --- Sensor Schemas ---


class SensorBase(BaseModel):
    serial_number: str
    type: str


class SensorCreate(SensorBase):
    node_id: Optional[int] = None


class SensorUpdate(BaseModel):
    serial_number: Optional[str] = None
    type: Optional[str] = None
    node_id: Optional[int] = None


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
    name: Optional[str] = None


class NodeCreate(NodeBase):
    pass


class NodeUpdate(BaseModel):
    serial_number: Optional[str] = None
    name: Optional[str] = None


class NodeBasic(NodeBase):
    id: int

    class Config:
        orm_mode = True


class Node(NodeBasic):
    sensors: List[Sensor] = []   # List of attached sensors
