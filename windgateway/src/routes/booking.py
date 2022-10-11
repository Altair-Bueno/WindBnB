from fastapi import APIRouter, Depends

from src.model.booking import Booking, CreateBooking
from ..service import BookingService

router = APIRouter()


@router.post("/")
async def create_booking(request: CreateBooking,
                         service: BookingService = Depends(BookingService)) -> Booking:
    return await service.new_booking(request)


@router.get("/{booking_id}")
async def get_booking(booking_id: str,
                      service: BookingService = Depends(BookingService)) -> Booking:
    return await service.get_booking_by_id(booking_id)


@router.delete("/{booking_id}")
async def cancel_booking(booking_id: str,
                         service: BookingService = Depends(BookingService)):
    return await service.cancel_booking(booking_id)
