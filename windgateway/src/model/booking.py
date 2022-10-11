from datetime import date

from pydantic.dataclasses import dataclass


@dataclass
class Booking:
    id: str
    startDate: date
    endDate: date


@dataclass
class CreateBooking:
    startDate: date
    endDate: date
