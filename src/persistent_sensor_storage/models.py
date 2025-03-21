from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class NodeSensorAssociation(Base):
    __tablename__ = "node_sensor_association"
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer, ForeignKey('nodes.id'))
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    status = Column(String)

    # Define relationships
    node = relationship("Node", back_populates="associations")
    sensor = relationship("Sensor", back_populates="associations")


class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    firmware_version = Column(String, nullable=False)

    # One-to-many relationship to NodeSensorAssociation
    associations = relationship("NodeSensorAssociation", back_populates="node")

    # Many-to-many relationship using the rich association table
    sensors = relationship(
        "Sensor", 
        secondary=NodeSensorAssociation.__table__, 
        back_populates="nodes"
    )


class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True)
    manufacturer = Column(String, nullable=False)
    model = Column(String, nullable=False)
    modality = Column(String, nullable=False)

    # One-to-many relationship to NodeSensorAssociation
    associations = relationship(
        "NodeSensorAssociation", back_populates="sensor")

    # Define relationship to nodes through the association table
    nodes = relationship(
        "Node", 
        secondary=NodeSensorAssociation.__table__, 
        back_populates="sensors"
    )
