from datetime import date
from enum import Enum
from typing import Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, root_validator, validator

from src.model.types import PyObjectId


class BookingStateEnum(str, Enum):
    reserved = "reserved"
    canceled = "canceled"


class Booking(BaseModel):
    """Contains all the known information about a booking"""
    id: PyObjectId
    house_id: PyObjectId
    user_id: str
    start_date: date
    end_date: date
    state: BookingStateEnum = BookingStateEnum.reserved

    class Config:
        json_encoders = {ObjectId: str}


class NewBooking(BaseModel):
    """Payload for creating new bookings"""
    house_id: PyObjectId
    user_id: str
    start_date: date
    end_date: date

    @root_validator
    def valid_date(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")

        if start_date >= end_date:
            raise ValueError("Cannot end booking on a past date")

        return values

    @validator("start_date")
    def no_past_reservations(cls, v):
        if date.today() <= v:
            return v
        else:
            raise ValueError("Cannot book on a past date")

    class Config:
        json_encoders = {ObjectId: str}


class SortBookingEnum(str, Enum):
    start_date = "start_date"
    end_date = "end_date"


class FilterBooking(BaseModel):
    """Payload for filtering bookings"""
    user_id: Optional[str]
    owner_id: Optional[str]
    house_id: Optional[PyObjectId]
    state: Optional[BookingStateEnum]
    before_date: Optional[date]
    after_date: Optional[date]
    skip: Optional[int]
    sort_by: Optional[SortBookingEnum]
    ascending = False

    class Config:
        json_encoders = {ObjectId: str}
