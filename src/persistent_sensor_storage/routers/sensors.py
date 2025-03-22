from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("/", response_model=List[schemas.Sensor])
def read_sensors(
    manufacturer: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    modality: Optional[str] = Query(None),
    node_id: Optional[str] = Query(None),
    skip: int = 0,
    limit: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    sensors = crud.get_sensors(
        db,
        offset=skip,
        limit=limit,
        manufacturer=manufacturer,
        model=model,
        modality=modality,
        node_id=node_id
    )
    return sensors


@router.get("/{sensor_id}", response_model=schemas.Sensor)
def read_sensor(sensor_id: str, db: Session = Depends(get_db)):
    sensor = crud.get_sensor(db, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.post("/", response_model=schemas.Sensor, status_code=201)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    # Only check for duplicate serial if one is provided
    if sensor.serial_number:
        db_sensor = crud.get_sensor_by_serial(
            db, serial_number=sensor.serial_number
        )
        if db_sensor:
            raise HTTPException(
                status_code=400,
                detail="Sensor already registered"
            )
    
    # Validate required fields
    if not all([sensor.manufacturer, sensor.model, sensor.modality]):
        raise HTTPException(
            status_code=400,
            detail="Manufacturer, model, and modality are required"
        )
    
    return crud.create_sensor(db=db, sensor=sensor)


@router.put("/{sensor_id}", response_model=schemas.Sensor)
def update_sensor(
    sensor_id: str,
    sensor_update: schemas.SensorUpdate,
    db: Session = Depends(get_db)
):
    db_sensor = crud.update_sensor(db, sensor_id, sensor_update)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor


@router.patch("/{sensor_id}", response_model=schemas.Sensor)
def partial_update_sensor(
    sensor_id: str,
    sensor_update: schemas.SensorUpdate,
    db: Session = Depends(get_db)
):
    db_sensor = crud.update_sensor(db, sensor_id, sensor_update)
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db_sensor
