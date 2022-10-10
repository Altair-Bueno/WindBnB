from fastapi import APIRouter
from .booking import router as bookingRouter

BaseRouter = APIRouter()

BaseRouter.include_router(bookingRouter, prefix="/booking")

@BaseRouter.get("/ping")
async def ping():
    return {
        "message": "OK"
    }