from sqlalchemy.orm import Session
from . import models, schemas

# --- Node CRUD Operations ---


def get_node(db: Session, node_id: int):
    return db.query(models.Node).filter(models.Node.id == node_id).first()


def get_node_by_serial(db: Session, serial_number: str):
    return db.query(models.Node).filter(models.Node.serial_number == serial_number).first()


def get_nodes(db: Session, skip: int = 0, limit: int = 100, serial_number: str = None):
    query = db.query(models.Node)
    if serial_number:
        query = query.filter(models.Node.serial_number == serial_number)
    return query.offset(skip).limit(limit).all()


def create_node(db: Session, node: schemas.NodeCreate):
    db_node = models.Node(**node.dict())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node


def update_node(db: Session, node_id: int, node_update: schemas.NodeUpdate):
    db_node = get_node(db, node_id)
    if not db_node:
        return None
    update_data = node_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_node, key, value)
    db.commit()
    db.refresh(db_node)
    return db_node

# --- Sensor CRUD Operations ---


def get_sensor(db: Session, sensor_id: int):
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()


def get_sensor_by_serial(db: Session, serial_number: str):
    return db.query(models.Sensor).filter(models.Sensor.serial_number == serial_number).first()


def get_sensors(db: Session, skip: int = 0, limit: int = 100, sensor_type: str = None, node_id: int = None):
    query = db.query(models.Sensor)
    if sensor_type:
        query = query.filter(models.Sensor.type == sensor_type)
    if node_id is not None:
        query = query.filter(models.Sensor.node_id == node_id)
    return query.offset(skip).limit(limit).all()


def create_sensor(db: Session, sensor: schemas.SensorCreate):
    db_sensor = models.Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def update_sensor(db: Session, sensor_id: int, sensor_update: schemas.SensorUpdate):
    db_sensor = get_sensor(db, sensor_id)
    if not db_sensor:
        return None
    update_data = sensor_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sensor, key, value)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def attach_sensor_to_node(db: Session, node_id: int, sensor_id: int):
    db_node = get_node(db, node_id)
    db_sensor = get_sensor(db, sensor_id)
    if not db_node or not db_sensor:
        return None
    db_sensor.node_id = node_id
    db.commit()
    db.refresh(db_sensor)
    return db_sensor
