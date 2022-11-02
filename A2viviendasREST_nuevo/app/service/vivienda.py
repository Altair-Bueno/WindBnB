from turtle import title
from typing import Collection
from bson import ObjectId
import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection
from requests import request
from app.models.vivienda import viviendaStateEnum
from app.models.vivienda import Vivienda
from app.models.vivienda import NewVivienda

class ViviendaService:
    collection: AsyncIOMotorCollection

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def new_vivienda(self, request: NewVivienda) -> Vivienda:
        Vivienda_id = ObjectId()
        
        result = await self.collection.update_one(
            {
                "_id": Vivienda_id,
                "title": request.title,
                "description": request.description,
                "user_id": request.user_id,
                "location": request.location,
                "state": viviendaStateEnum.available.value
            }) 
            
        if result.modified_count == 1:
            return Vivienda(
                title= request.title,
                description= request.description,
                user_id= request.user_id,
                location= request.location,
                state= viviendaStateEnum.available
            )

        '''async def delete_house(self, idCasa: str):
        result = await self.collection.update_one(
            {"bookings._id": booking_id},
            {"$set": {
                "bookings.$[booking].state": BookingStateEnum.canceled.value}},
        )

        if result.modified_count == 0:
            raise NotFoundError(
                f"Couldn't find any reserved bookings to cancel. {booking_id=}")'''
