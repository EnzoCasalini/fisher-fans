from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import enum


# Définir les énumérations comme en Python natif
class StatusEnum(str, enum.Enum):
    individual = 'individual'
    professional = 'professional'


class ActivityTypeEnum(str, enum.Enum):
    rental = 'rental'
    fishing_guide = 'fishing guide'


class LicenseTypeEnum(str, enum.Enum):
    coastal = 'coastal'
    river = 'river'


class BoatTypeEnum(str, enum.Enum):
    open = 'open'
    cabin = 'cabin'
    catamaran = 'catamaran'
    sailboat = 'sailboat'
    jet_ski = 'jet ski'
    canoe = 'canoe'


class EquipmentEnum(str, enum.Enum):
    sonar = 'sonar'
    livewell = 'livewell'
    ladder = 'ladder'
    GPS = 'GPS'
    rod_holders = 'rod holders'
    VHF_radio = 'VHF radio'


class EngineTypeEnum(str, enum.Enum):
    diesel = 'diesel'
    gasoline = 'gasoline'
    none = 'none'


class TripTypeEnum(str, enum.Enum):
    daily = 'daily'
    recurring = 'recurring'


class RateTypeEnum(str, enum.Enum):
    total = 'total'
    per_person = 'per person'


# Définir les tables
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    email = Column(String, unique=True, nullable=False)
    boat_license = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), nullable=True)
    company_name = Column(String, nullable=True)
    activity_type = Column(Enum(ActivityTypeEnum), nullable=True)
    siret_number = Column(String, nullable=True)
    rc_number = Column(String, nullable=True)

    # Relations
    boats = relationship("Boat", back_populates="owner")
    trips = relationship("Trip", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")
    log = relationship("Log", uselist=False, back_populates="owner")


class Boat(Base):
    __tablename__ = "boats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    manufacture_year = Column(Date, nullable=True)
    photo_url = Column(String, nullable=True)
    license_type = Column(Enum(LicenseTypeEnum), nullable=True)
    boat_type = Column(Enum(BoatTypeEnum), nullable=True)
    deposit_amount = Column(Float, nullable=True)
    max_capacity = Column(Integer, nullable=True)
    number_of_beds = Column(Integer, nullable=True)
    home_port = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    engine_type = Column(Enum(EngineTypeEnum), nullable=True)
    engine_power = Column(Integer, nullable=True)

    # Relations
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="boats")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    practical_info = Column(String, nullable=True)
    trip_type = Column(Enum(TripTypeEnum), nullable=True)
    rate_type = Column(Enum(RateTypeEnum), nullable=True)
    passenger_count = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)

    # Dates
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    departure_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    # Relations
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="trips")
    boat_id = Column(Integer, ForeignKey("boats.id"), nullable=False)
    boat = relationship("Boat", back_populates="trips")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    reserved_seats = Column(Integer, nullable=True)
    total_price = Column(Float, nullable=True)

    # Relations
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="reservations")
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    trip = relationship("Trip", back_populates="reservations")


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    # Relations
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="log")
    pages = relationship("Page", back_populates="log")


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    fish_name = Column(String, nullable=True)
    fish_photo_url = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    length = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    fishing_spot = Column(String, nullable=True)
    fishing_date = Column(Date, nullable=True)
    release = Column(Boolean, nullable=True)

    # Relations
    log_id = Column(Integer, ForeignKey("logs.id"), nullable=False)
    log = relationship("Log", back_populates="pages")