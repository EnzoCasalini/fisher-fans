from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum as SQLAlchemyEnum
from .models import Status, LicenseType, BoatType, EngineType
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
    boats = relationship("Boat", back_populates="owner")
    reservations = relationship("Reservation", back_populates="user")

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
    equipment = Column(String, nullable=True)  # Stocker en tant que liste sérialisée (JSON, par exemple)
    depositAmount = Column(Float, nullable=True)
    maxCapacity = Column(Integer, nullable=True)
    numberOfBeds = Column(Integer, nullable=True)
    homePort = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    engineType = Column(SQLAlchemyEnum(EngineType, name="engine_type_enum"), nullable=True)
    enginePower = Column(Integer, nullable=True)

    trips = relationship("Trip", back_populates="boats")
 
    # Relation avec User (si un bateau est associé à un utilisateur)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)  # ForeignKey vers l'utilisateur propriétaire
    owner = relationship("User", back_populates="boats")



class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, index=True)
    tripId = Column(String, ForeignKey("trips.id"), nullable=False)  # Correspond à trip
    date = Column(Date, nullable=False)
    reservedSeats = Column(Integer, nullable=False)
    totalPrice = Column(Float, nullable=False)
    userId = Column(String, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="reservations")
