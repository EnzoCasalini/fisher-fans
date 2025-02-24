from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Secret key to sign JWT tokens
SECRET_KEY = "f505f74b6e93be31f0fff4cc18ee76e62d38c82a161bdc2b535680c7e6a8f9b95d9be718ce18fd7be4deef1286e066c86318cb0fe846cfa3712cf8a263938a71dd80c18c65273e9f9927e45dd41851b01413efaa191996709f5b6f43d14a4c685fd3aa3c5505d265eb0e849501f79020089451b284ad5868d366eae7cc1594c2409191fab5ff12872e1cba0ff12507fef659ae9edab63d0a8d1c1a5c56ff41ac6adba02c48be8264b79ccfa7a5b5b200096d6efca5bec7a5784389fa6fe77a6eb76409faf5cbf7200ba63283091e845f0e998fe11744780ef98e64303352a7bc576b02d04c1d051ca7701d973ed7b4b54cd3e1b9283dd02d2aada391bd261a93"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
