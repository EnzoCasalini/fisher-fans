from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models_sqlalchemy import User as SQLAlchemyUser
from app.auth.auth_utils import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

router = APIRouter(tags=["Authentication"])

# Definition of OAuth2PasswordBearer to extract the token in requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


def authenticate_user(db: Session, login: str, password: str):
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.login == login).first()
    if not user:
        return False
    if not verify_password(password, user.hashedPassword):
        return False
    return user


@router.post("/v1/token", summary="Get a JWT token to access protected endpoints.")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, login=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> SQLAlchemyUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str | None = payload.get("sub")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.login == login).first()
    if user is None:
        raise credentials_exception
    return user
