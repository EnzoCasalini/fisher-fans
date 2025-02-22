from __future__ import annotations

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import UserRead, UserCreate, Error
from app.models_sqlalchemy import User as SQLAlchemyUser
from app.routers.auth import get_current_user
from app.auth.auth_utils import get_password_hash
from app.dependencies import get_db

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
    company: Optional[str] = None,  # Filtre optionnel par companyName
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> List[UserRead]:
    query = db.query(SQLAlchemyUser)
    if company:
        query = query.filter(SQLAlchemyUser.companyName.ilike(f"%{company}%"))
    users = query.offset(skip).limit(limit).all()
    return [UserRead.from_orm(user) for user in users]


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
)
def get_user(user_id: str, db: Session = Depends(get_db)) -> UserRead:
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Transformation du champ id en chaîne de caractères
    user_dict = user.__dict__
    user_dict['id'] = str(user_dict['id'])
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
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: SQLAlchemyUser = Depends(get_current_user)
) -> None:
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
