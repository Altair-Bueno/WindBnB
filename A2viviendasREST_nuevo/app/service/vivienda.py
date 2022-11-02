import re
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
        document = request.dict()
        document["state"] = viviendaStateEnum.available.value
        
        result = await self.collection.insert_one(document) 
            
        if result.inserted_id:
            return Vivienda(
                id = result.inserted_id,
                **document
                # Te falta el id result.inserted_id
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
