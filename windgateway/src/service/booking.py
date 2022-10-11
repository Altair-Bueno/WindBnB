from fastapi import Depends

from src.beans import get_windbnb_collection
from src.model.booking import Booking, CreateBooking


class BookingService:
    def __init__(self, windbnb=Depends(get_windbnb_collection)):
        self.windbnb = windbnb

    async def get_booking_by_id(self, booking_id: str) -> Booking:
        pass

    async def new_booking(self, request: CreateBooking) -> Booking:
        pass

    async def cancel_booking(self, booking_id: str):
        pass
