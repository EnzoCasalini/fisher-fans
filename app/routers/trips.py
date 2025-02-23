from __future__ import annotations

import uuid
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Trip as PydanticTrip
from app.models_sqlalchemy import Trip as SQLAlchemyTrip
import json
from datetime import date

from ..dependencies import get_db, Error

router = APIRouter(tags=['Trips'])

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
    user_id: Optional[str] = Query(None, alias='userId'),
    title: Optional[str] = None,
    trip_type: Optional[str] = Query(None, alias='tripType'),
    start_date: Optional[date] = Query(None, alias='startDate'),
    end_date: Optional[date] = Query(None, alias='endDate'),
    db: Session = Depends(get_db)
) -> Union[List[PydanticTrip], Error]:
    """
    Get a list of trips
    """
    query = db.query(SQLAlchemyTrip)
    
    if user_id:
        query = query.filter(SQLAlchemyTrip.user_id == user_id)
    if title:
        query = query.filter(SQLAlchemyTrip.title.ilike(f"%{title}%"))
    if trip_type:
        query = query.filter(SQLAlchemyTrip.tripType == trip_type)
    if start_date:
        query = query.filter(SQLAlchemyTrip.startDates.contains(json.dumps(start_date.isoformat())))
    if end_date:
        query = query.filter(SQLAlchemyTrip.endDates.contains(json.dumps(end_date.isoformat())))
    
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
        '403': {'model': Error},
        '422': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Trips'],
)
def create_trip(trip: PydanticTrip, db: Session = Depends(get_db)):
    if not trip.id:
        trip.id = str(uuid.uuid4())

    if any(end < start for start, end in zip(trip.startDates, trip.endDates)):
        raise HTTPException(status_code=400, detail="End date cannot be before start date.")

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
    db_trip = db.query(SQLAlchemyTrip).filter(SQLAlchemyTrip.id == tripId).first()
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
    db_trip = db.query(SQLAlchemyTrip).filter(SQLAlchemyTrip.id == tripId).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if db_trip.reservations:
        raise HTTPException(status_code=409, detail="Cannot delete a trip with active reservations.")
    
    db.delete(db_trip)
    db.commit()
    
    return None