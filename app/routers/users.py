from __future__ import annotations

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models import UserRead, UserCreate, Error
from app.models_sqlalchemy import User as SQLAlchemyUser
from app.routers.auth import get_current_user
from app.auth.auth_utils import get_password_hash
from app.models_sqlalchemy import (
    User as SQLAlchemyUser,
)

from ..dependencies import get_db, Error

router = APIRouter(tags=['Users'])


# Endpoint protégé : récupérer l'utilisateur connecté
@router.get("/v1/users/me", response_model=UserRead, summary="Get the current user's information.")
def read_users_me(current_user: SQLAlchemyUser = Depends(get_current_user)):
    return UserRead.from_orm(current_user)


# Endpoint public : récupérer la liste des utilisateurs
@router.get(
    '/v1/users',
    response_model=List[UserRead],
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
) -> List[UserRead]:
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
            "id": user.log.id if user.log else None,
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
                for page in user.log.pages
            ] if user.log else []
        } if user.log else None

        result.append(UserRead(**user_dict))

    return result

# Endpoint public : inscription / création d'un utilisateur
@router.post(
    '/v1/users',
    response_model=UserRead,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Users'],
)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    # Générer un UUID si aucun ID n'est fourni
    if not user.id:
        user.id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    db_user = SQLAlchemyUser(
        id=user.id,
        login=user.login,
        hashedPassword=hashed_password,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        status=user.status,
        birthDate=user.birthDate,
        companyName=user.companyName,
        boatLicense=user.boatLicense,
        activityType=user.activityType,
        siretNumber=user.siretNumber,
        rcNumber=user.rcNumber,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserRead.from_orm(db_user)


# Endpoint public : récupérer un utilisateur par ID
@router.get(
    '/v1/users/{user_id}',
    response_model=UserRead,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Users'],
)
def get_user(user_id: str, db: Session = Depends(get_db)) -> UserRead:
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Transformation du champ id en chaîne de caractères
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
        "id": user.log.id if user.log else None,
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
            for page in user.log.pages
        ] if user.log else []
    } if user.log else None

    return UserRead(**user_dict)


# Endpoint protégé : mettre à jour un utilisateur (authentification requise)
@router.put(
    '/v1/users/{user_id}',
    response_model=UserRead,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '404': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Users'],
)
def update_user(
    user_id: str,
    updated_user: UserRead,
    db: Session = Depends(get_db),
    current_user: SQLAlchemyUser = Depends(get_current_user)  # Ici, l'utilisateur doit être authentifié
) -> UserRead:
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Mise à jour des champs (vous pouvez ajouter une vérification pour s'assurer que current_user est autorisé)

    for key, value in updated_user.dict(exclude_unset=True, exclude={"boats", "trips", "reservations", "log"}).items():
        setattr(user, key, value)

    # Sauvegarder les modifications
    db.commit()
    db.refresh(user)
    return UserRead.from_orm(user)


# Endpoint protégé : supprimer un utilisateur (authentification requise)
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
    tags=['Users'],
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    # current_user: SQLAlchemyUser = Depends(get_current_user)
) -> None:
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # if user.reservations:
    #     raise HTTPException(status_code=409, detail="Cannot delete user with active reservations.")

    # Anonymisation des données personnelles
    user.login = f"anonymised_{user.id}"
    user.firstName = None
    user.lastName = None
    user.email = None
    user.boatLicense = None
    # Maybe remove other fields as well
    user.isAnonymised = True

    db.commit()
    return None
