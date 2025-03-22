from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas, crud
from ..dependencies import get_db

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get("/", response_model=List[schemas.NodeResponse])
def read_nodes(
    serial_number: Optional[str] = Query(None),
    firmware_version: Optional[str] = Query(None),
    skip: int = 0,
    limit: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    nodes = crud.get_nodes(
        db,
        skip=skip,
        limit=limit,
        serial_number=serial_number,
        firmware_version=firmware_version
    )
    return nodes


@router.get("/{node_id}", response_model=schemas.NodeResponse)
def read_node(node_id: str, db: Session = Depends(get_db)):
    node = crud.get_node(db, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.post("/", response_model=schemas.NodeResponse, status_code=201)
def create_node(node: schemas.NodeCreate, db: Session = Depends(get_db)):
    # Only check for duplicate serial if one is provided
    if node.serial_number:
        db_node = crud.get_node_by_serial(
            db, serial_number=node.serial_number
        )
        if db_node:
            raise HTTPException(
                status_code=400,
                detail="Node already registered"
            )
    
    # Validate required fields
    if not node.firmware_version:
        raise HTTPException(
            status_code=400,
            detail="Firmware version is required"
        )
    
    return crud.create_node(db=db, node=node)


@router.put("/{node_id}", response_model=schemas.NodeResponse)
def update_node(
    node_id: str,
    node_update: schemas.NodeUpdate,
    db: Session = Depends(get_db)
):
    db_node = crud.update_node(
        db, node_id, node_update)
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    return db_node


@router.patch("/{node_id}", response_model=schemas.NodeResponse)
def partial_update_node(
    node_id: str,
    node_update: schemas.NodeUpdate,
    db: Session = Depends(get_db)
):
    db_node = crud.update_node(db, node_id, node_update)
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    return db_node


@router.get("/{node_id}/full", response_model=schemas.Node)
def read_node_with_sensors(node_id: str, db: Session = Depends(get_db)):
    """Get a node with its associated sensors."""
    node = crud.get_node(db, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.post("/{node_id}/sensors", response_model=schemas.SensorResponse)
def attach_sensor(
    node_id: str,
    sensor_request: schemas.SensorAttachRequest,
    db: Session = Depends(get_db)
):
    sensor = crud.attach_sensor_to_node(
        db, node_id, sensor_request.sensor_id
    )
    if not sensor:
        raise HTTPException(
            status_code=404,
            detail="Node or Sensor not found"
        )
    return sensor
