# generated by fastapi-codegen:
#   filename:  FF_API.yaml
#   timestamp: 2024-11-22T13:36:24+00:00

from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import UserRead as PydanticUser
from app.models_sqlalchemy import User as SQLAlchemyUser


from ..dependencies import *

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
    tags=['Users'],
)
def get_users(
    lastName: Optional[str] = Query(None, description="Filter by last name"),
    firstName: Optional[str] = Query(None, description="Filter by first name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    status: Optional[str] = Query(None, description="Filter by status", enum=[
                                  "individual", "professional"]),
    company: Optional[str] = Query(None, description="Filter by company name"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> List[PydanticUser]:
    """
    Récupère une liste d'utilisateurs avec pagination et filtres multiples.
    """
    query = db.query(SQLAlchemyUser)

    # Appliquer les filtres
    if lastName:
        query = query.filter(SQLAlchemyUser.lastName.ilike(f"%{lastName}%"))
    if firstName:
        query = query.filter(SQLAlchemyUser.firstName.ilike(f"%{firstName}%"))
    if email:
        query = query.filter(SQLAlchemyUser.email.ilike(f"%{email}%"))
    if status:
        query = query.filter(SQLAlchemyUser.status == status)

    # Appliquer la pagination
    users = query.offset(skip).limit(limit).all()

    # Retourner la liste formatée avec Pydantic
    return [PydanticUser.from_orm(user) for user in users]


@router.post(
    '/v1/users',
    response_model=None,
    responses={
        '400': {'model': Error},
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
    tags=['Users'],
)
def create_user(user: PydanticUser, db: Session = Depends(get_db)) -> Optional[Error]:
    # Générer un UUID si aucun ID n'est fourni
    if not user.id:
        user.id = str(uuid.uuid4())

    db_user = SQLAlchemyUser(
        id=user.id,  # UUID généré ici
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
    tags=['Users'],
)
def get_user(user_id: str, db: Session = Depends(get_db)) -> PydanticUser:
    user = db.query(SQLAlchemyUser).filter(
        SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Convertir en dictionnaire et transformer `id` en string
    user_dict = user.__dict__
    user_dict['id'] = str(user_dict['id'])
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
    tags=['Users'],
)
def update_user(user_id: str, updated_user: PydanticUser, db: Session = Depends(get_db)) -> PydanticUser:
    """
    Met à jour les informations d'un utilisateur spécifique par son ID.
    """
    # Rechercher l'utilisateur à mettre à jour
    user = db.query(SQLAlchemyUser).filter(
        SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mettre à jour les champs
    user.firstName = updated_user.firstName or user.firstName
    user.lastName = updated_user.lastName or user.lastName
    user.email = updated_user.email or user.email
    user.status = updated_user.status or user.status
    user.birthDate = updated_user.birthDate or user.birthDate
    user.companyName = updated_user.companyName or user.companyName
    user.boatLicense = updated_user.boatLicense or user.boatLicense
    user.activityType = updated_user.activityType or user.activityType
    user.siretNumber = updated_user.siretNumber or user.siretNumber
    user.rcNumber = updated_user.rcNumber or user.rcNumber

    # Sauvegarder les modifications
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
    tags=['Users'],
)
def delete_user(user_id: str, db: Session = Depends(get_db)) -> None:
    """
    Supprime un utilisateur spécifique par son ID.
    """
    # Rechercher l'utilisateur à supprimer
    user = db.query(SQLAlchemyUser).filter(
        SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Supprimer l'utilisateur
    db.delete(user)
    db.commit()

    return None  # Retourne un code 204 (No Content)
