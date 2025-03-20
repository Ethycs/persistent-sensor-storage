from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    
    # A node can have multiple sensors
    sensors = relationship("Sensor", back_populates="node")

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    type = Column(String, nullable=False)
    
    # Optional association to a node
    node_id = Column(Integer, ForeignKey("nodes.id"), nullable=True)
    node = relationship("Node", back_populates="sensors")
