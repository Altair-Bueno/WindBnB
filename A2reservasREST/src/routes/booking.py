from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import conint

from ..auth import Authentication, Claims

from ..beans import get_booking_service
from ..model import *
from ..service import *

router = APIRouter()

NOT_FOUND_RESPONSE = {404: {"model": ApiError}}
ALREADY_BOOKED_RESPONSE = {409: {"model": ApiError}}


@router.get("", response_model=List[Booking], operation_id="get_bookings")
async def get_bookings(
    before_date: Optional[date] = None,
    after_date: Optional[date] = None,
    skip: Optional[conint(ge=0)] = None,
    sort_by: Optional[SortBookingEnum] = None,
    ascending: Optional[bool] = False,
    house_id: Optional[PyObjectId] = None,
    owner_id: Optional[PyObjectId] = None,
    state: Optional[BookingStateEnum] = None,
    service: BookingService = Depends(get_booking_service),
    auth: Claims = Depends(Authentication),
):
    """Returns a list of bookings that match the given criteria. 10 bookings max"""
    f = FilterBooking(
        before_date=before_date,
        after_date=after_date,
        skip=skip,
        sort_by=sort_by,
        ascending=ascending,
        house_id=house_id,
        owner_id=owner_id,
        state=state,
    )
    return await service.get_bookings(auth, f)


@router.post(
    "",
    response_model=PaypalCreateOrderRequestBody,
    operation_id="new_booking",
    responses=ALREADY_BOOKED_RESPONSE,
)
async def create_booking(
    request: NewBooking,
    service: BookingService = Depends(get_booking_service),
    auth: Claims = Depends(Authentication),
):
    """Creates a new booking"""
    try:
        return await service.new_booking(auth, request)
    except AlreadyBookedError as e:
        raise HTTPException(status_code=409, detail=e.error_code)


@router.put(
    "/{booking_id}/capture",
    response_model=Booking,
    operation_id="capture_booking_payment",
    responses=NOT_FOUND_RESPONSE,
)
async def capture_booking_payment(
    booking_id: PyObjectId,
    order_id: str,
    service: BookingService = Depends(get_booking_service),
    auth: Claims = Depends(Authentication),
):
    """Updates an existing booking"""
    try:
        return await service.update_booking(auth, booking_id, order_id)
    except UpdateBookingError as e:
        raise HTTPException(status_code=404, detail=e.error_code)


@router.get(
    "/{booking_id}",
    response_model=Booking,
    operation_id="get_booking_by_id",
    responses=NOT_FOUND_RESPONSE,
)
async def get_booking_by_id(
    booking_id: PyObjectId,
    service: BookingService = Depends(get_booking_service),
    auth: Claims = Depends(Authentication),
):
    """Returns all the information related to the given `booking_id`"""
    try:
        return await service.get_booking_by_id(auth, booking_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.error_code)


@router.delete(
    "/{booking_id}",
    response_model=Message,
    operation_id="cancel_booking",
    responses=NOT_FOUND_RESPONSE,
)
async def cancel_booking(
    booking_id: PyObjectId,
    service: BookingService = Depends(get_booking_service),
    auth: Claims = Depends(Authentication),
):
    """Cancels the booking identified by the given `booking_id`"""
    try:
        await service.cancel_booking(auth, booking_id)
        return Message(message="Successfully canceled booking")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.error_code)
