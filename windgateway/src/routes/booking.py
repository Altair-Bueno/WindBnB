from fastapi import APIRouter, Depends

from ..service import BookingService

router = APIRouter()

@router.post("/")
async def create_booking():
    return {}

@router.get("/{bookingId}")
async def get_booking(bookingId: str, bookingService: BookingService = Depends(BookingService)):
    return await bookingService.getBooking(bookingId)

@router.delete("/{bookingId}")
async def cancel_booking(bookingId: str, bookingService: BookingService = Depends(BookingService)):
    return await bookingService.cancelBooking(bookingId)
