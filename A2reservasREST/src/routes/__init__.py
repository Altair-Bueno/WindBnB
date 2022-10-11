from fastapi import APIRouter

from .booking import router as booking_router
from ..model import Message

BaseRouter = APIRouter()

BaseRouter.include_router(booking_router, prefix="/booking")


@BaseRouter.get("/ping", response_model=Message)
async def ping():
    return Message(message="Available")
