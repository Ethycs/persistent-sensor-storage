from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import uuid


class NodeSensorAssociation(Base):
    __tablename__ = "node_sensor_association"
    id = Column(
        String,
        primary_key=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    sensor_id = Column(String, ForeignKey('sensors.id'), nullable=False)
    status = Column(String)

    # Define relationships
    node = relationship("Node", back_populates="associations")
    sensor = relationship("Sensor", back_populates="associations")


class Node(Base):
    __tablename__ = "nodes"
    id = Column(
        String,
        primary_key=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    serial_number = Column(String, unique=True, index=True, nullable=True)
    firmware_version = Column(String, nullable=False)

    # One-to-many relationship to NodeSensorAssociation
    associations = relationship("NodeSensorAssociation", back_populates="node")

    # Many-to-many relationship using the rich association table
    sensors = relationship(
        "Sensor", 
        secondary=NodeSensorAssociation.__table__, 
        back_populates="nodes",
        overlaps="associations,node"
    )


class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(
        String,
        primary_key=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    serial_number = Column(String, unique=True, index=True, nullable=True)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    modality = Column(String, nullable=False)
    node_id = Column(String, ForeignKey('nodes.id'), nullable=True)

    # One-to-many relationship to NodeSensorAssociation
    associations = relationship(
        "NodeSensorAssociation", 
        back_populates="sensor",
        overlaps="sensors"
    )

    # Define relationship to nodes through the association table
    nodes = relationship(
        "Node", 
        secondary=NodeSensorAssociation.__table__, 
        back_populates="sensors",
        overlaps="associations,node"
    )
