from typing import List

from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from ..beans import get_booking_service
from ..model import Message
from ..model.booking import *
from ..service import BookingService

router = APIRouter()


@router.get("", response_model=List[Booking])
async def get_bookings(
    user_id: Optional[str] = None,
    before_date: Optional[date] = None,
    after_date: Optional[date] = None,
    skip: Optional[PositiveInt] = None,
    sort_by: Optional[SortBookingEnum] = None,
    ascending: Optional[bool] = False,
    house_id: Optional[str] = None,
    state: Optional[BookingStateEnum] = None,
    service: BookingService = Depends(get_booking_service),
):
    f = FilterBooking(
        user_id=user_id,
        before_date=before_date,
        after_date=after_date,
        skip=skip,
        sort_by=sort_by,
        ascending=ascending,
        house_id=house_id,
        state=state,
    )
    return await service.get_bookings(f)


@router.post("", response_model=Booking)
async def create_booking(
    request: NewBooking, service: BookingService = Depends(get_booking_service)
):
    return await service.new_booking(request)


@router.get("/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: str, service: BookingService = Depends(get_booking_service)
):
    return await service.get_booking_by_id(booking_id)


@router.delete("/{booking_id}", response_model=Message)
async def cancel_booking(
    booking_id: str, service: BookingService = Depends(get_booking_service)
):
    await service.cancel_booking(booking_id)
    return Message(message=f"Successfully canceled {booking_id}")
