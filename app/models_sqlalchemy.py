from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum as SQLAlchemyEnum
from .models import Status, LicenseType, BoatType, EngineType
from sqlalchemy.orm import relationship
from app.db import Base
from sqlalchemy import Boolean

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

    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    boats = relationship("Boat", back_populates="owner", cascade="all, delete-orphan")
    log = relationship("Log", back_populates="user", cascade="all, delete-orphan", uselist=False)
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")

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
    boat_id = Column(String, ForeignKey("boats.id"))

    user = relationship("User", back_populates="trips")
    boats = relationship("Boat", back_populates="trips")
    reservations = relationship("Reservation", back_populates="trip")

class Boat(Base):
    __tablename__ = "boats"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    manufactureYear = Column(String, nullable=True)
    photoUrl = Column(String, nullable=True)
    licenseType = Column(SQLAlchemyEnum(LicenseType, name="license_type_enum"), nullable=True)
    boatType = Column(SQLAlchemyEnum(BoatType, name="boat_type_enum"), nullable=True)
    equipment = Column(String, nullable=True)
    depositAmount = Column(Float, nullable=True)
    maxCapacity = Column(Integer, nullable=True)
    numberOfBeds = Column(Integer, nullable=True)
    homePort = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    engineType = Column(SQLAlchemyEnum(EngineType, name="engine_type_enum"), nullable=True)
    enginePower = Column(Integer, nullable=True)

    trips = relationship("Trip", back_populates="boats")
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="boats")

class Log(Base):
    __tablename__ = "log"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="log")
    pages = relationship("Page", back_populates="log", cascade="all, delete-orphan")

class Page(Base):
    __tablename__ = "pages"

    id = Column(String, primary_key=True, index=True)
    log_id = Column(String, ForeignKey("log.id"), nullable=False)
    fish_name = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    size_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    dateOfCatch = Column(Date, nullable=True)
    released = Column(Boolean, nullable=False)

    log = relationship("Log", back_populates="pages")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, index=True)
    tripId = Column(String, ForeignKey("trips.id"), nullable=False)  # Correspond à trip
    date = Column(Date, nullable=False)
    reservedSeats = Column(Integer, nullable=False)
    totalPrice = Column(Float, nullable=False)
    userId = Column(String, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="reservations")
    trip = relationship("Trip", back_populates="reservations")