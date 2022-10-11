from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, root_validator


class Booking(BaseModel):
    id: str
    house_id: str
    user: str
    start_date: date
    end_date: date


class NewBooking(BaseModel):
    house_id: str
    user: str
    start_date: date
    end_date: date

    @root_validator
    def valid_date(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")

        if start_date > end_date:
            raise ValueError("Invalid start date")

        return values


class SortBookingEnum(str, Enum):
    start_date = "start_date"
    end_date = "end_date"


class FilterBooking(BaseModel):
    user: Optional[str]
    before_date: Optional[date]
    after_date: Optional[date]
    skip: Optional[int]
    sort_by: Optional[SortBookingEnum]
    ascending = False
