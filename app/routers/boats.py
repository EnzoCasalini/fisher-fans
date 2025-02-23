# generated by fastapi-codegen:
#   filename:  FF_API.yaml
#   timestamp: 2024-11-22T13:36:24+00:00

from __future__ import annotations

import uuid
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.models import Boat as PydanticBoat
from app.models_sqlalchemy import Boat as SQLAlchemyBoat
from ..dependencies import *

router = APIRouter(tags=['Boats'])


@router.get(
    '/v1/boats',
    response_model=List[PydanticBoat],
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Boats'],
)
def get_boats(
    user_id: Optional[str] = Query(None, alias='userId'),
    name: Optional[str] = None,
    brand: Optional[str] = None,
    boat_type: Optional[str] = Query(None, alias='boatType'),
    home_port: Optional[str] = Query(None, alias='homePort'),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> List[PydanticBoat]:
    """
    Get the list of boats with optional filters and pagination.
    """
    query = db.query(SQLAlchemyBoat)

    if user_id:
        query = query.filter(SQLAlchemyBoat.owner_id == user_id)
    if name:
        query = query.filter(SQLAlchemyBoat.name.ilike(f"%{name}%"))
    if brand:
        query = query.filter(SQLAlchemyBoat.brand.ilike(f"%{brand}%"))
    if boat_type:
        query = query.filter(SQLAlchemyBoat.boatType.ilike(f"%{boat_type}%"))
    if home_port:
        query = query.filter(SQLAlchemyBoat.homePort.ilike(f"%{home_port}%"))

    boats = query.offset(skip).limit(limit).all()

    # Convert fields that need to be strings
    for boat in boats:
        if isinstance(boat.manufactureYear, str):
            boat.manufactureYear = str(boat.manufactureYear)
        if isinstance(boat.depositAmount, float):
            boat.depositAmount = str(boat.depositAmount)
        if isinstance(boat.latitude, float):
            boat.latitude = str(boat.latitude)
        if isinstance(boat.longitude, float):
            boat.longitude = str(boat.longitude)

    return [PydanticBoat.from_orm(boat) for boat in boats]

@router.post('/v1/boats', response_model=None)
def create_boat(boat: PydanticBoat, db: Session = Depends(get_db)) -> None:
    # Vérifier si un bateau avec le même ID existe déjà
    existing_boat = db.query(SQLAlchemyBoat).filter(SQLAlchemyBoat.id == boat.id).first()
    if existing_boat:
        raise HTTPException(status_code=409, detail="Boat with this ID already exists.")

    if not boat.id:
        boat.id = str(uuid.uuid4())

    db_boat = SQLAlchemyBoat(**boat.dict())
    db.add(db_boat)
    db.commit()
    db.refresh(db_boat)

@router.get('/v1/boats/bbox', response_model=List[PydanticBoat])
def get_boats_by_bbox(
    lat_min: float = Query(..., description="Minimum latitude"),
    lat_max: float = Query(..., description="Maximum latitude"),
    lon_min: float = Query(..., description="Minimum longitude"),
    lon_max: float = Query(..., description="Maximum longitude"),
    db: Session = Depends(get_db),
) -> List[PydanticBoat]:
    if lat_min > lat_max or lon_min > lon_max:
        raise HTTPException(status_code=400, detail="Invalid bounding box: lat_min must be ≤ lat_max and lon_min ≤ lon_max")

    query = db.query(SQLAlchemyBoat).filter(
        SQLAlchemyBoat.latitude >= lat_min, SQLAlchemyBoat.latitude <= lat_max,
        SQLAlchemyBoat.longitude >= lon_min, SQLAlchemyBoat.longitude <= lon_max
    )
    boats = query.all()

    if not boats:
        raise HTTPException(status_code=404, detail="No boats found in the specified area.")

    return [PydanticBoat.from_orm(boat) for boat in boats]  # ✅ Retourne 404 si aucun bateau trouvé

from uuid import UUID

@router.get('/v1/boats/{boat_id}', response_model=PydanticBoat)
def get_boat_by_id(boat_id: str, db: Session = Depends(get_db)) -> PydanticBoat:
    try:
        UUID(boat_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid boat ID format")

    boat = db.query(SQLAlchemyBoat).filter(SQLAlchemyBoat.id == boat_id).first()
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")

    return PydanticBoat.from_orm(boat)

@router.put(
    '/v1/boats/{boat_id}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Boats'],
)
def update_boat(
    boat_id: str, boat: PydanticBoat, db: Session = Depends(get_db)
) -> Optional[Error]:
    """
    Edit a boat.
    """
    db_boat = db.query(SQLAlchemyBoat).filter(SQLAlchemyBoat.id == boat_id).first()
    if not db_boat:
        raise HTTPException(status_code=404, detail="Boat not found")

    for key, value in boat.dict(exclude_unset=True).items():
        setattr(db_boat, key, value)

    db.commit()
    db.refresh(db_boat)
    return None


@router.delete(
    '/v1/boats/{boat_id}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Boats'],
)
def delete_boat(boat_id: str, db: Session = Depends(get_db)) -> Optional[Error]:
    """
    Delete a boat.
    """
    db_boat = db.query(SQLAlchemyBoat).filter(SQLAlchemyBoat.id == boat_id).first()
    if not db_boat:
        raise HTTPException(status_code=404, detail="Boat not found")

    db.delete(db_boat)
    db.commit()
    return None
