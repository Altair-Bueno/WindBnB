from fastapi import APIRouter

from .booking import router as booking_router
from ..model import Message

BaseRouter = APIRouter()

BaseRouter.include_router(booking_router, prefix="/booking", tags=["Booking"])


@BaseRouter.get("/ping", response_model=Message, tags=["Booking"])
async def ping():
    """Responds with an "Available" message, if the service is available"""
    return Message(message="Available")
