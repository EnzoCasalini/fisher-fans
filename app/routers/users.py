from __future__ import annotations

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models import UserRead as PydanticUser
from app.models_sqlalchemy import (
    User as SQLAlchemyUser,
)

from ..dependencies import get_db, Error

router = APIRouter(tags=['Users'])

@router.get(
    '/v1/users',
    response_model=List[PydanticUser],
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
)
def get_users(
    lastName: Optional[str] = Query(None, description="Filter by last name"),
    firstName: Optional[str] = Query(None, description="Filter by first name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    status: Optional[str] = Query(None, description="Filter by status", enum=["individual", "professional"]),
    company: Optional[str] = Query(None, description="Filter by company name"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> List[PydanticUser]:
    """
    Récupère une liste d'utilisateurs avec pagination et filtres multiples.
    """
    query = db.query(SQLAlchemyUser)

    # Apply filters
    if lastName:
        query = query.filter(SQLAlchemyUser.lastName.ilike(f"%{lastName}%"))
    if firstName:
        query = query.filter(SQLAlchemyUser.firstName.ilike(f"%{firstName}%"))
    if email:
        query = query.filter(SQLAlchemyUser.email.ilike(f"%{email}%"))
    if status:
        query = query.filter(SQLAlchemyUser.status == status)
    if company:
        query = query.filter(SQLAlchemyUser.companyName.ilike(f"%{company}%"))

    users = query.offset(skip).limit(limit).all()

    result = []
    for user in users:
        user_dict = user.__dict__.copy()
        user_dict['id'] = str(user.id)

        # Add boats
        user_dict["boats"] = [
            {
                "id": boat.id,
                "name": boat.name,
                "brand": boat.brand,
                "homePort": boat.homePort,
            }
            for boat in user.boats
        ] if user.boats else None

        # Add trips
        user_dict["trips"] = [
            {
                "id": trip.id,
                "title": trip.title,
                "tripType": trip.tripType,
                "price": trip.price,
            }
            for trip in user.trips
        ] if user.trips else None

        # Add reservations
        user_dict["reservations"] = [
            {
                "id": res.id,
                "tripId": res.tripId,
                "date": res.date,
                "reservedSeats": res.reservedSeats,
                "totalPrice": res.totalPrice,
                "userId": res.userId,
            }
            for res in user.reservations
        ]

        # Add fishing log pages
        user_dict["log"] = {
            "id": user.log[0].id if user.log else None,
            "pages": [
                {
                    "id": page.id,
                    "fish_name": page.fish_name,
                    "photo_url": page.photo_url,
                    "comment": page.comment,
                    "size_cm": page.size_cm,
                    "weight_kg": page.weight_kg,
                    "location": page.location,
                    "dateOfCatch": page.dateOfCatch,
                    "released": page.released,
                }
                for page in user.log[0].pages
            ] if user.log else []
        } if user.log else None

        result.append(PydanticUser(**user_dict))

    return result

@router.post(
    '/v1/users',
    response_model=PydanticUser,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
)
def create_user(user: PydanticUser, db: Session = Depends(get_db)) -> PydanticUser:
    """
    Crée un nouvel utilisateur.
    """
    if not user.id:
        user.id = str(uuid.uuid4())

    db_user = SQLAlchemyUser(**user.dict(exclude={"boats", "trips", "reservations", "log"}))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return PydanticUser.from_orm(db_user)

@router.get(
    '/v1/users/{user_id}',
    response_model=PydanticUser,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
)
def get_user(user_id: str, db: Session = Depends(get_db)) -> PydanticUser:
    """
    Récupère un utilisateur par son ID avec ses bateaux, trips, réservations et son log de pêche.
    """
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = user.__dict__.copy()
    user_dict['id'] = str(user.id)

    # Add boats
    user_dict["boats"] = [
        {
            "id": boat.id,
            "name": boat.name,
            "brand": boat.brand,
            "homePort": boat.homePort,
        }
        for boat in user.boats
    ] if user.boats else None

    # Add trips
    user_dict["trips"] = [
        {
            "id": trip.id,
            "title": trip.title,
            "tripType": trip.tripType,
            "price": trip.price,
        }
        for trip in user.trips
    ] if user.trips else None

    # Add reservations
    user_dict["reservations"] = [
        {
            "id": res.id,
            "tripId": res.tripId,
            "date": res.date,
            "reservedSeats": res.reservedSeats,
            "totalPrice": res.totalPrice,
            "userId": res.userId,
        }
        for res in user.reservations
    ]

    # Add fishing log pages
    user_dict["log"] = {
        "id": user.log[0].id if user.log else None,
        "pages": [
            {
                "id": page.id,
                "fish_name": page.fish_name,
                "photo_url": page.photo_url,
                "comment": page.comment,
                "size_cm": page.size_cm,
                "weight_kg": page.weight_kg,
                "location": page.location,
                "dateOfCatch": page.dateOfCatch,
                "released": page.released,
            }
            for page in user.log[0].pages
        ] if user.log else []
    } if user.log else None

    return PydanticUser(**user_dict)

@router.put(
    '/v1/users/{user_id}',
    response_model=PydanticUser,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
)
def update_user(user_id: str, updated_user: PydanticUser, db: Session = Depends(get_db)) -> PydanticUser:
    """
    Met à jour les informations d'un utilisateur spécifique par son ID.
    """
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_user.dict(exclude_unset=True, exclude={"boats", "trips", "reservations", "log"}).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return PydanticUser.from_orm(user)

@router.delete(
    '/v1/users/{user_id}',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
)
def delete_user(user_id: str, db: Session = Depends(get_db)) -> None:
    """
    Supprime un utilisateur spécifique par son ID.
    """
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.reservations:
        raise HTTPException(status_code=409, detail="Cannot delete user with active reservations.")

    db.delete(user)
    db.commit()
    return None