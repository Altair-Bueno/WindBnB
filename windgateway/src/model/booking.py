from pydantic.dataclasses import dataclass
from datetime import date

@dataclass
class Booking:
    id: str
    startDate: date
    endDate: date
