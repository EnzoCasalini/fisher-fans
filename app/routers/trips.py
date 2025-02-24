from __future__ import annotations

import uuid
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Trip as PydanticTrip
from app.models_sqlalchemy import Trip as SQLAlchemyTrip
from app.models_sqlalchemy import Boat as SQLAlchemyBoat
from app.models_sqlalchemy import User as SQLAlchemyUser
import json
from datetime import date
from datetime import datetime
from sqlalchemy import func
from ..dependencies import get_db, Error
from app.routers.auth import get_current_user


router = APIRouter(
    tags=['Trips'],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    '/v1/trips',
    response_model=List[PydanticTrip],
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Trips'],
)
def get_v1_trips(
    userId: Optional[str] = Query(None, description="Filter trips by user"),
    title: Optional[str] = Query(None, description="Filter trips by title"),
    tripType: Optional[str] = Query(None, description="Filter trips by type"),
    startDates: Optional[List[date]] = Query(
        None, description="Filter trips by start dates"),
    endDates: Optional[List[date]] = Query(
        None, description="Filter trips by end dates"),
    db: Session = Depends(get_db)
) -> Union[List[PydanticTrip], Error]:
    """
    Get a list of trips with optional filters, including multiple start and end dates
    """
    query = db.query(SQLAlchemyTrip)

    if userId:
        query = query.filter(SQLAlchemyTrip.user_id == userId)
    if title:
        query = query.filter(SQLAlchemyTrip.title.ilike(f"%{title}%"))
    if tripType:
        query = query.filter(SQLAlchemyTrip.tripType == tripType)
    if startDates:
        start_date_conditions = [
            SQLAlchemyTrip.startDates.like(f'%{date.isoformat()}%')
            for date in startDates
        ]
        query = query.filter(or_(*start_date_conditions))
    if endDates:
        end_date_conditions = [
            SQLAlchemyTrip.endDates.like(f'%{date.isoformat()}%')
            for date in endDates
        ]
        query = query.filter(or_(*end_date_conditions))

    trips = query.all()

    return [PydanticTrip(
        **{**trip.__dict__,
           'startDates': json.loads(trip.startDates),
           'endDates': json.loads(trip.endDates),
           'departureTimes': json.loads(trip.departureTimes),
           'endTimes': json.loads(trip.endTimes)
           }) for trip in trips]



@router.post(
    '/v1/trips',
    response_model=PydanticTrip,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},  # 👈 Ajout de la réponse 403
        '422': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Trips'],
)
def create_trip(trip: PydanticTrip, db: Session = Depends(get_db)):
    """
    Create a new fishing trip.
    """

    # Vérifier si l'utilisateur possède un bateau
    has_boat = db.query(SQLAlchemyBoat).filter(SQLAlchemyBoat.owner_id == trip.user_id).first()

    if not has_boat:
        raise HTTPException(status_code=403, detail="You cannot create a fishing trip without owning a boat.")

    if not trip.id:
        trip.id = str(uuid.uuid4())

    db_trip = SQLAlchemyTrip(
        id=trip.id,
        title=trip.title,
        practicalInfo=trip.practicalInfo,
        tripType=trip.tripType,
        rateType=trip.rateType,
        startDates=json.dumps([d for d in trip.startDates]),
        endDates=json.dumps([d for d in trip.endDates]),
        departureTimes=json.dumps([t for t in trip.departureTimes]),
        endTimes=json.dumps([t for t in trip.endTimes]),
        passengerCount=trip.passengerCount,
        price=trip.price,
        user_id=trip.user_id
    )

    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    trip_dict = db_trip.__dict__
    trip_dict['startDates'] = json.loads(trip_dict['startDates'])
    trip_dict['endDates'] = json.loads(trip_dict['endDates'])
    trip_dict['departureTimes'] = json.loads(trip_dict['departureTimes'])
    trip_dict['endTimes'] = json.loads(trip_dict['endTimes'])

    return PydanticTrip(**trip_dict)


@router.get(
    '/v1/trips/{tripId}',
    response_model=PydanticTrip,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Trips'],
)
def get_v1_trips_trip_id(
    tripId: str = Path(..., alias='tripId'),
    db: Session = Depends(get_db)
) -> Union[PydanticTrip, Error]:
    """
    Get a trip by ID
    """
    trip = db.query(SQLAlchemyTrip).filter(SQLAlchemyTrip.id == tripId).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip_dict = trip.__dict__
    trip_dict['startDates'] = json.loads(trip_dict['startDates'])
    trip_dict['endDates'] = json.loads(trip_dict['endDates'])
    trip_dict['departureTimes'] = json.loads(trip_dict['departureTimes'])
    trip_dict['endTimes'] = json.loads(trip_dict['endTimes'])

    return PydanticTrip(**trip_dict)


@router.put(
    '/v1/trips/{tripId}',
    response_model=PydanticTrip,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Trips'],
)
def put_v1_trips_trip_id(
    tripId: str = Path(..., alias='tripId'),
    trip: PydanticTrip = ...,
    db: Session = Depends(get_db)
) -> Union[PydanticTrip, Error]:
    """
    Edit a trip
    """
    db_trip = db.query(SQLAlchemyTrip).filter(
        SQLAlchemyTrip.id == tripId).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    for key, value in trip.dict(exclude_unset=True).items():
        if key in ['startDates', 'endDates', 'departureTimes', 'endTimes']:
            setattr(db_trip, key, json.dumps(value))
        else:
            setattr(db_trip, key, value)

    db.commit()
    db.refresh(db_trip)

    trip_dict = db_trip.__dict__
    trip_dict['startDates'] = json.loads(trip_dict['startDates'])
    trip_dict['endDates'] = json.loads(trip_dict['endDates'])
    trip_dict['departureTimes'] = json.loads(trip_dict['departureTimes'])
    trip_dict['endTimes'] = json.loads(trip_dict['endTimes'])

    return PydanticTrip(**trip_dict)


@router.delete(
    '/v1/trips/{tripId}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Trips'],
)
def delete_v1_trips_trip_id(
    tripId: str = Path(..., alias='tripId'),
    db: Session = Depends(get_db)
) -> Optional[Error]:
    """
    Delete a trip
    """
    db_trip = db.query(SQLAlchemyTrip).filter(
        SQLAlchemyTrip.id == tripId).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if db_trip.reservations:
        raise HTTPException(status_code=409, detail="Cannot delete a trip with active reservations.")
    
    db.delete(db_trip)
    db.commit()

    return None
