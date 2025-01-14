from sqlalchemy import Column, Integer, String, Date, Enum as SQLAlchemyEnum
from .models import Status
from sqlalchemy.orm import relationship
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    lastName = Column(String, index=True)
    firstName = Column(String, index=True)
    birthDate = Column(Date, nullable=True)
    email = Column(String, unique=True, index=True)
    boatLicense = Column(String, nullable=True)
    status = Column(SQLAlchemyEnum(Status), nullable=True)
    companyName = Column(String, nullable=True)
    activityType = Column(String, nullable=True)
    siretNumber = Column(String, nullable=True)
    rcNumber = Column(String, nullable=True)