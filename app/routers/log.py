from __future__ import annotations

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.models import Log as PydanticLog, Page as PydanticPage
from app.models_sqlalchemy import Log as SQLAlchemyLog, Page as SQLAlchemyPage, User
from ..dependencies import *
from app.routers.auth import get_current_user


router = APIRouter(
    tags=['Log'],
    dependencies=[Depends(get_current_user)]
)

@router.get("/v1/log/{user_id}", response_model=PydanticLog)
def get_user_log(user_id: str = Path(...), db: Session = Depends(get_db)) -> PydanticLog:
    """
    Get a user's fishing log
    """
    log = db.query(SQLAlchemyLog).filter(SQLAlchemyLog.user_id == user_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return PydanticLog.model_validate(log)

@router.post("/v1/log/{user_id}", response_model=PydanticLog, status_code=201)
def create_user_log(user_id: str = Path(...), db: Session = Depends(get_db)) -> PydanticLog:
    """
    Create a fishing log for a user
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_log = SQLAlchemyLog(id=str(uuid.uuid4()), user_id=user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return PydanticLog.from_orm(db_log)

@router.get("/v1/log/{user_id}/pages", response_model=List[PydanticPage])
def get_log_pages(user_id: str = Path(...), db: Session = Depends(get_db)) -> List[PydanticPage]:
    """
    Get all pages of a user's fishing log
    """
    log = db.query(SQLAlchemyLog).filter(SQLAlchemyLog.user_id == user_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return [PydanticPage.model_validate(page) for page in log.pages]

@router.get("/v1/log/{user_id}/pages/{page_id}", response_model=PydanticPage)
def get_log_page(user_id: str = Path(...), page_id: str = Path(...), db: Session = Depends(get_db)) -> PydanticPage:
    """
    Get a page of a user's fishing log
    """
    page = db.query(SQLAlchemyPage).filter(SQLAlchemyPage.id == page_id, SQLAlchemyPage.log.has(user_id=user_id)).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return PydanticPage.model_validate(page)

@router.post("/v1/log/{user_id}/pages", response_model=PydanticPage, status_code=201)
def add_log_page(
    user_id: str = Path(...),
    page: Optional[PydanticPage] = None,
    db: Session = Depends(get_db)
) -> PydanticPage:
    """
    Add a page to a user's fishing log
    """
    if page is None:
        raise HTTPException(status_code=400, detail="Page content is required")

    log = db.query(SQLAlchemyLog).filter(SQLAlchemyLog.user_id == user_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    if page.size_cm < 0 or page.weight_kg < 0:
        raise HTTPException(status_code=400, detail="Size and weight cannot be negative.")

    db_page = SQLAlchemyPage(
        id=str(uuid.uuid4()),  # ✅ Génération d'un UUID
        log_id=log.id,
        fish_name=page.fish_name,
        photo_url=page.photo_url,
        comment=page.comment,
        size_cm=page.size_cm,
        weight_kg=page.weight_kg,
        location=page.location,
        dateOfCatch=page.dateOfCatch,
        released=page.released
    )

    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return PydanticPage.model_validate(db_page)
@router.put("/v1/log/{user_id}/pages/{page_id}", response_model=PydanticPage)
def update_log_page(
        user_id: str = Path(...),
        page_id: str = Path(...),
        page: PydanticPage = ...,
        db: Session = Depends(get_db)
) -> PydanticPage:
    """
    Edit a page of a user's fishing log
    """
    db_page = db.query(SQLAlchemyPage).filter(SQLAlchemyPage.id == page_id, SQLAlchemyPage.log.has(user_id=user_id)).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")

    for key, value in page.model_dump(exclude_unset=True).items():
        setattr(db_page, key, value)

    db.commit()
    db.refresh(db_page)
    return PydanticPage.model_validate(db_page)

@router.delete("/v1/log/{user_id}/pages/{page_id}", status_code=204)
def delete_log_page(user_id: str = Path(...), page_id: str = Path(...),
                    db: Session = Depends(get_db)) -> None:
    """
    Delete a page from a user's fishing log
    """
    db_page = db.query(SQLAlchemyPage).filter(SQLAlchemyPage.id == page_id, SQLAlchemyPage.log.has(user_id=user_id)).first()
    if not db_page:
        raise HTTPException(status_code=404, detail="Page not found")

    db.delete(db_page)
    db.commit()
    return None
