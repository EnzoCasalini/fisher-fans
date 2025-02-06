from sqlalchemy import Column, Integer, String, Date, Enum as SQLAlchemyEnum, ForeignKey, Float
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
    trips = relationship("Trip", back_populates="user")

class Trip(Base):
    __tablename__ = "trips"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    practicalInfo = Column(String)
    tripType = Column(String)
    rateType = Column(String)
    startDates = Column(String)
    endDates = Column(String)
    departureTimes = Column(String)
    endTimes = Column(String)
    passengerCount = Column(Integer)
    price = Column(Float)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="trips")
    