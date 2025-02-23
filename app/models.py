# generated by fastapi-codegen:
#   filename:  FF_API.yaml
#   timestamp: 2024-11-22T13:36:24+00:00

from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional

from pydantic import AnyUrl, BaseModel, EmailStr, Field


class Error(BaseModel):
    code: str
    message: str


class Status(Enum):
    individual = 'individual'
    professional = 'professional'


class ActivityType(Enum):
    rental = 'rental'
    fishing_guide = 'fishing guide'


class LicenseType(Enum):
    coastal = 'coastal'
    river = 'river'


class BoatType(Enum):
    open = 'open'
    cabin = 'cabin'
    catamaran = 'catamaran'
    sailboat = 'sailboat'
    jet_ski = 'jet ski'
    canoe = 'canoe'


class EquipmentEnum(Enum):
    sonar = 'sonar'
    livewell = 'livewell'
    ladder = 'ladder'
    GPS = 'GPS'
    rod_holders = 'rod holders'
    VHF_radio = 'VHF radio'


class EngineType(Enum):
    diesel = 'diesel'
    gasoline = 'gasoline'
    none = 'none'


class Boat(BaseModel):
    id: Optional[str] = Field(None, description='Unique identifier of the boat')
    name: Optional[str] = Field(None, description='Name of the boat')
    description: Optional[str] = Field(None, description='Description of the boat')
    brand: Optional[str] = Field(None, description='Brand of the boat')
    manufactureYear: Optional[str] = Field(
        None, description='Year the boat was manufactured'
    )
    photoUrl: Optional[str] = Field(None, description="URL of the boat's photo")
    licenseType: Optional[LicenseType] = Field(
        None, description='Required license type (coastal or river)'
    )
    boatType: Optional[BoatType] = Field(None, description='Type of boat')
    equipment: Optional[str] = Field(
        None,
        description='List of equipment on board (e.g., sonar, livewell, ladder, GPS, rod holders, VHF radio)',
    )
    depositAmount: Optional[float] = Field(
        None, description='Deposit amount (in euros)'
    )
    maxCapacity: Optional[int] = Field(None, description='Maximum number of passengers')
    numberOfBeds: Optional[int] = Field(None, description='Number of beds on the boat')
    homePort: Optional[str] = Field(None, description='Home port (city name)')
    latitude: Optional[float] = Field(None, description='Latitude of the home port')
    longitude: Optional[float] = Field(None, description='Longitude of the home port')
    engineType: Optional[EngineType] = Field(
        None, description='Type of engine (diesel, gasoline, or none)'
    )
    enginePower: Optional[int] = Field(None, description='Engine power (in horsepower)')
    owner_id: Optional[str] = Field(None, description='ID of the owner (user)')

    class Config:
        from_attributes = True  # Permet l'utilisation de from_orm

class Trip(BaseModel):
    id: Optional[str] = Field(None, description='Unique identifier of the trip')
    title: Optional[str] = Field(None, description='Title of the trip')
    practicalInfo: Optional[str] = Field(None, description='Practical information about the trip')
    tripType: Optional[TripType] = Field(None, description='Type of trip (daily or recurring)')
    rateType: Optional[RateType] = Field(None, description='Type of rate (total or per person)')
    startDates: Optional[List[str]] = Field(None, description='List of start dates for the trip')
    endDates: Optional[List[str]] = Field(None, description='List of end dates for the trip')
    departureTimes: Optional[List[str]] = Field(None, description='List of departure times')
    endTimes: Optional[List[str]] = Field(None, description='List of end times')
    passengerCount: Optional[int] = Field(None, description='Number of passengers')
    price: Optional[float] = Field(None, description='Price of the trip')
    user_id: Optional[str] = Field(None, description='ID of the user associated with this trip')

    class Config:
        from_attributes = True


class Reservation(BaseModel):
    id: Optional[str] = Field(None, description='Unique identifier of the reservation')
    trip: Optional[Trip] = None
    date: Optional[datetime] = None
    reservedSeats: Optional[int] = None
    totalPrice: Optional[float] = None
    userId: Optional[str] = Field(None, description='User who made the reservation')

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: Optional[str] = Field(None, description='Unique identifier of the user')
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    birthDate: Optional[date] = None
    email: Optional[EmailStr] = None
    boatLicense: Optional[str] = Field(
        None, description='Boat license number (8 digits)'
    )
    status: Optional[Status] = Field(
        None, description='Status of the user (individual or professional)'
    )
    companyName: Optional[str] = Field(
        None, description='Company name (empty if individual)'
    )
    activityType: Optional[str] = Field(
        None, description='Type of activity (rental or fishing guide)'
    )
    siretNumber: Optional[str] = Field(None, description='SIRET number')
    rcNumber: Optional[str] = Field(None, description='Commercial register number (RC)')
    boats: Optional[List[Boat]] = None
    trips: Optional[List[Trip]] = None
    reservations: Optional[List[Reservation]] = None
    log: Optional[Log] = None

    class Config:
        from_attributes = True

class TripType(str, Enum):
    daily = 'daily'
    recurring = 'recurring'

class RateType(str, Enum):
    total = 'total'
    per_person = 'per person'


class Log(BaseModel):
    id: Optional[str] = Field(None, description='Unique identifier of the fishing log')
    user_id: Optional[str] = Field(None, description='ID of the user owning the log')
    pages: list["Page"] = []  # ✅ Correction pour éviter la récursion

    class Config:
        from_attributes = True


class Page(BaseModel):
    id: Optional[str] = Field(None, description='Unique identifier of the fishing log page')
    log_id: Optional[str] = Field(None, description='ID of the fishing log')
    fish_name: Optional[str] = Field(None, description='Name of the fish')
    photo_url: Optional[str] = Field(None, description='URL of the fish photo')
    comment: Optional[str] = Field(None, description='Comment about the catch')
    size_cm: Optional[float] = Field(None, description='Size of the fish in cm')
    weight_kg: Optional[float] = Field(None, description='Weight of the fish in kg')
    location: Optional[str] = Field(None, description='Fishing location')
    dateOfCatch: Optional[date] = Field(None, description='Date of the catch')
    released: Optional[bool] = Field(None, description='Was the fish released?')

    class Config:
        from_attributes = True


# ✅ Évite les erreurs de récursion
UserRead.update_forward_refs()
UserRead.model_rebuild()
Log.model_rebuild()
Page.model_rebuild()