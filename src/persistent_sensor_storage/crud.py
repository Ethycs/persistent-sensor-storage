from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas
import uuid

# --- Node CRUD Operations ---


def get_node(db: Session, node_id: str):
    return (
        db.query(models.Node)
        .filter(models.Node.id == node_id)
        .first()
    )


def get_node_by_serial(db: Session, serial_number: str):
    return (
        db.query(models.Node)
        .filter(models.Node.serial_number == serial_number)
        .first()
    )


def get_nodes(
    db: Session,
    offset: int = 0,
    limit: Optional[int] = None,
    serial_number: str = None,
    firmware_version: str = None
):
    actual_offset = offset
    query = db.query(models.Node)
    if serial_number:
        query = query.filter(models.Node.serial_number == serial_number)
    if firmware_version:
        query = query.filter(models.Node.firmware_version == firmware_version)
    if limit is not None:
        query = query.limit(limit)
    return query.offset(actual_offset).all()


def create_node(db: Session, node: schemas.NodeCreate):
    # Use provided ID or generate UUID
    node_data = node.model_dump()
    if not node_data.get('id'):
        node_data['id'] = str(uuid.uuid4())
    
    db_node = models.Node(**node_data)
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


def update_node(db: Session, node_id: str, node_update: schemas.NodeUpdate):
    db_node = get_node(db, node_id)
    if not db_node:
        return None
    update_data = node_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_node, key, value)
    db.commit()
    db.refresh(db_node)
    return db_node

# --- Sensor CRUD Operations ---


def get_sensor(db: Session, sensor_id: str):
    result = (
        db.query(models.Sensor)
        .outerjoin(models.NodeSensorAssociation)
        .with_entities(
            models.Sensor,
            models.NodeSensorAssociation.node_id
        )
        .filter(models.Sensor.id == sensor_id)
        .first()
    )
    if not result:
        return None
    
    sensor, node_id = result
    return schemas.SensorResponse(
        **sensor.__dict__,
        node_id=node_id
    )


def get_sensor_by_serial(db: Session, serial_number: str):
    result = (
        db.query(models.Sensor)
        .outerjoin(models.NodeSensorAssociation)
        .with_entities(
            models.Sensor,
            models.NodeSensorAssociation.node_id
        )
        .filter(models.Sensor.serial_number == serial_number)
        .first()
    )
    if not result:
        return None
    
    sensor, node_id = result
    return schemas.SensorResponse(
        **sensor.__dict__,
        node_id=node_id
    )


def get_sensors(
    db: Session,
    offset: int = 0,
    limit: Optional[int] = None,
    manufacturer: str = None,
    model: str = None,
    modality: str = None,
    node_id: str = None
):
    query = (
        db.query(models.Sensor)
        .outerjoin(models.NodeSensorAssociation)
        .with_entities(
            models.Sensor,
            models.NodeSensorAssociation.node_id
        )
    )
    
    # Apply filters
    if manufacturer:
        query = query.filter(models.Sensor.manufacturer == manufacturer)
    if model:
        query = query.filter(models.Sensor.model == model)
    if modality:
        query = query.filter(models.Sensor.modality == modality)
    if node_id:
        query = query.filter(models.NodeSensorAssociation.node_id == node_id)
    
    # Apply pagination
    if limit is not None:
        query = query.limit(limit)
    
    results = query.offset(offset).all()
    return [
        schemas.SensorResponse(
            **sensor.__dict__,
            node_id=node_id
        )
        for sensor, node_id in results
    ]


def create_sensor(db: Session, sensor: schemas.SensorCreate):
    # Use provided ID or generate UUID
    sensor_data = sensor.model_dump()
    if not sensor_data.get('id'):
        sensor_data['id'] = str(uuid.uuid4())
    
    db_sensor = models.Sensor(**sensor_data)
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    
    return schemas.SensorResponse(
        **db_sensor.__dict__,
        node_id=None
    )


def update_sensor(
    db: Session,
    sensor_id: str,
    sensor_update: schemas.SensorUpdate
):
    result = (
        db.query(models.Sensor)
        .outerjoin(models.NodeSensorAssociation)
        .with_entities(
            models.Sensor,
            models.NodeSensorAssociation.node_id
        )
        .filter(models.Sensor.id == sensor_id)
        .first()
    )
    if not result:
        return None
    
    sensor, node_id = result
    update_data = sensor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sensor, key, value)
    db.commit()
    db.refresh(sensor)
    
    return schemas.SensorResponse(
        **sensor.__dict__,
        node_id=node_id
    )


def attach_sensor_to_node(db: Session, node_id: str, sensor_id: str):
    db_node = get_node(db, node_id)
    db_sensor = (
        db.query(models.Sensor)
        .filter(models.Sensor.id == sensor_id)
        .first()
    )
    if not db_node or not db_sensor:
        return None
    
    # Create association with UUID
    association = models.NodeSensorAssociation(
        id=str(uuid.uuid4()),
        node_id=node_id,
        sensor_id=sensor_id
    )
    
    # Add association and commit
    db.add(association)
    db.commit()
    db.refresh(db_sensor)
    
    return schemas.SensorResponse(
        **db_sensor.__dict__,
        node_id=node_id
    )
