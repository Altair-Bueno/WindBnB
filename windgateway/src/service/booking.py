from fastapi import Depends
from pydantic import BaseModel
from src.beans import MongoClient

from src.model.booking import Booking

class BookingService:
    mongoClient = Depends(MongoClient)
    
    async def getBooking(booking: str) -> Booking:
        pass

    async def newBooking():
        pass
    
    async def cancelBooking():
        pass
