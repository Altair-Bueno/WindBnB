from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt

from ..model.types import ApiError

from ..service.error import *

from ..beans import get_booking_service
from ..model import Message
from ..model.booking import *
from ..service import BookingService

router = APIRouter()

NOT_FOUND_RESPONSE = {
    404: {"model": ApiError}
}
ALREADY_BOOKED_RESPONSE = {
    409: {"model": ApiError}
}

@router.get("", response_model=List[Booking], operation_id="get_bookings")
async def get_bookings(
    user_id: Optional[str] = None,
    before_date: Optional[date] = None,
    after_date: Optional[date] = None,
    skip: Optional[PositiveInt] = None,
    sort_by: Optional[SortBookingEnum] = None,
    ascending: Optional[bool] = False,
    house_id: Optional[PyObjectId] = None,
    owner_id: Optional[PyObjectId] = None,
    state: Optional[BookingStateEnum] = None,
    service: BookingService = Depends(get_booking_service),
):
    """Returns a list of bookings that match the given criteria. 10 bookings max"""
    f = FilterBooking(
        user_id=user_id,
        before_date=before_date,
        after_date=after_date,
        skip=skip,
        sort_by=sort_by,
        ascending=ascending,
        house_id=house_id,
        owner_id=owner_id,
        state=state,
    )
    return await service.get_bookings(f)


@router.post(
    "", 
    response_model=Booking, 
    operation_id="new_booking",
    responses=ALREADY_BOOKED_RESPONSE
)
async def create_booking(
    request: NewBooking, service: BookingService = Depends(get_booking_service)
):
    """Creates a new booking"""
    try:
        return await service.new_booking(request)
    except AlreadyBookedError as e:
        raise HTTPException(
            status_code=409, 
            detail=e.error_code
        )


@router.get(
    "/{booking_id}", 
    response_model=Booking, 
    operation_id="get_booking_by_id",
    responses=NOT_FOUND_RESPONSE
)
async def get_booking_by_id(
    booking_id: PyObjectId, service: BookingService = Depends(get_booking_service)
):
    """Returns all the information related to the given `booking_id`"""
    try: 
        return await service.get_booking_by_id(booking_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=404, 
            detail=e.error_code
        )



@router.delete(
    "/{booking_id}", 
    response_model=Message, 
    operation_id="cancel_booking", 
    responses=NOT_FOUND_RESPONSE
)
async def cancel_booking(
    booking_id: PyObjectId, service: BookingService = Depends(get_booking_service)
):
    """Cancels the booking identified by the given `booking_id`"""
    try: 
        await service.cancel_booking(booking_id)
        return Message(message=f"Successfully canceled booking")
    except NotFoundError as e:
        raise HTTPException(
            status_code=404, 
            detail=e.error_code
        )
