# generated by fastapi-codegen:
#   filename:  FF_API.yaml
#   timestamp: 2024-11-22T13:36:24+00:00

from __future__ import annotations

import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Path

import uuid
from app.models import Reservation as PydanticReservation
from app.models_sqlalchemy import Reservation as SQLAlchemyReservation
from app.models_sqlalchemy import Trip as SQLAlchemyTrip
from app.models_sqlalchemy import User as SQLAlchemyUser

from datetime import date
from ..dependencies import *
from app.routers.auth import get_current_user


router = APIRouter(
    tags=['Reservations'],
    dependencies=[Depends(get_current_user)]
)

@router.get(
    '/v1/reservations',
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Reservations'],
)
def get_reservations(
    db: Session = Depends(get_db),
    tripId: Optional[str] = Query(None, description="Filter by trip ID"),
    userId: Optional[str] = Query(None, description="Filter by user ID"),
    startDate: Optional[date] = Query(
        None, description="Filter reservations from this date"),
    endDate: Optional[date] = Query(
        None, description="Filter reservations up to this date"),
    minPrice: Optional[float] = Query(
        None, description="Filter reservations with minimum total price"),
    maxPrice: Optional[float] = Query(
        None, description="Filter reservations with maximum total price"),
    minSeats: Optional[int] = Query(
        None, description="Filter reservations with minimum number of reserved seats"),
    upcoming: Optional[bool] = Query(
        None, description="Filter only upcoming reservations")
) -> List[dict]:
    """
    Get the list of reservations with filters
    """
    query = db.query(SQLAlchemyReservation)

    # Apply filters
    if tripId:
        query = query.filter(SQLAlchemyReservation.tripId == tripId)
    if userId:
        query = query.filter(SQLAlchemyReservation.userId == userId)
    if startDate:
        query = query.filter(SQLAlchemyReservation.date >= startDate)
    if endDate:
        query = query.filter(SQLAlchemyReservation.date <= endDate)
    if minPrice:
        query = query.filter(SQLAlchemyReservation.totalPrice >= minPrice)
    if maxPrice:
        query = query.filter(SQLAlchemyReservation.totalPrice <= maxPrice)
    if minSeats:
        query = query.filter(SQLAlchemyReservation.reservedSeats >= minSeats)
    if upcoming:
        query = query.filter(SQLAlchemyReservation.date >= date.today())

    reservations = query.all()

    return [
        {
            "id": res.id,
            "tripId": res.tripId,
            "date": res.date,
            "reservedSeats": res.reservedSeats,
            "totalPrice": res.totalPrice,
            "userId": res.userId,
        }
        for res in reservations
    ]


@router.post(
    '/v1/reservations',
    status_code=201,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '422': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Reservations'],
)
def create_reservation(reservation: PydanticReservation, db: Session = Depends(get_db)):
    """
    Create a new reservation
    """
    if not reservation.id:
        reservation.id = str(uuid.uuid4())

    trip = db.query(SQLAlchemyTrip).filter(SQLAlchemyTrip.id ==
                                           reservation.trip.id).first() if reservation.trip else None
    if reservation.trip and not trip:
        raise HTTPException(status_code=400, detail="Trip does not exist")

    user = db.query(SQLAlchemyUser).filter(
        SQLAlchemyUser.id == reservation.userId).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if trip.user_id == reservation.userId:
        raise HTTPException(status_code=403, detail="You cannot book your own trip.")

    new_reservation = SQLAlchemyReservation(
        id=reservation.id,
        tripId=trip.id if trip else None,  # ✅ Stocke uniquement l'ID du trip
        date=reservation.date or datetime.utcnow(),
        reservedSeats=reservation.reservedSeats,
        totalPrice=reservation.totalPrice,
        userId=reservation.userId,
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return {
        "id": new_reservation.id,
        "tripId": new_reservation.tripId,  # ✅ Retourne uniquement l'ID
        "date": new_reservation.date,
        "reservedSeats": new_reservation.reservedSeats,
        "totalPrice": new_reservation.totalPrice,
        "userId": new_reservation.userId,
    }


@router.get(
    '/v1/reservations/{reservation_id}',
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Reservations'],
)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    """
    Get a reservation by ID with only the tripId
    """
    reservation = db.query(SQLAlchemyReservation).filter(
        SQLAlchemyReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return {
        "id": reservation.id,
        "tripId": reservation.tripId,  # ✅ Retourne uniquement l'ID du trip
        "date": reservation.date,
        "reservedSeats": reservation.reservedSeats,
        "totalPrice": reservation.totalPrice,
        "userId": reservation.userId,
    }


@router.put(
    '/v1/reservations/{reservation_id}',
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Reservations'],
)
def update_reservation(reservation_id: str, updated_reservation: PydanticReservation, db: Session = Depends(get_db)):
    """
    Edit a reservation
    """
    reservation = db.query(SQLAlchemyReservation).filter(
        SQLAlchemyReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    reservation.tripId = updated_reservation.trip.id if updated_reservation.trip else None
    reservation.date = updated_reservation.date or reservation.date
    reservation.reservedSeats = updated_reservation.reservedSeats
    reservation.totalPrice = updated_reservation.totalPrice
    reservation.userId = updated_reservation.userId

    db.commit()
    db.refresh(reservation)
    return {
        "id": reservation.id,
        "tripId": reservation.tripId,  # ✅ Retourne uniquement l'ID du trip
        "date": reservation.date,
        "reservedSeats": reservation.reservedSeats,
        "totalPrice": reservation.totalPrice,
        "userId": reservation.userId,
    }


@router.delete(
    '/v1/reservations/{reservation_id}',
    response_model=None,
    status_code=204,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Reservations'],
)
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    """
    Delete a reservation
    """
    reservation = db.query(SQLAlchemyReservation).filter(
        SQLAlchemyReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.date < datetime.utcnow().date():
        raise HTTPException(status_code=409, detail="Cannot delete past reservations.")

    db.delete(reservation)
    db.commit()
    return None
