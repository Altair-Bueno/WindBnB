from fastapi import APIRouter

from .booking import router as booking_router

BaseRouter = APIRouter()

BaseRouter.include_router(booking_router, prefix="/booking")


@BaseRouter.get("/ping")
async def ping():
    return {"message": "OK"}
