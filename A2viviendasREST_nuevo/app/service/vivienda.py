import re
from turtle import title
from typing import Collection, Optional
from bson import ObjectId
import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection
from requests import request
from app.service.error import NotFoundError
from app.models.types import PyObjectId
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
            
            )

    async def get_vivienda_by_id(self, idCasa: PyObjectId) -> Optional[Vivienda]:
        document = await self.collection.find_one(
            {"houses._id": idCasa},
            {"houses": {"$elemMatch": {"_id": idCasa}}}
        )
        if document:
            vivienda = document["houses"][0]
            return Vivienda(
                id=document["_id"],
                **vivienda
            )

    async def delete_house(self, idCasa: PyObjectId):
        result = await self.collection.update_one(
            {"houses._id": idCasa},
            {"$set": {
                "houses.$[Vivienda].state": viviendaStateEnum.deleted.value}}
        )

        if result.modified_count == 0:
            raise NotFoundError(
                f"Couldn't find any available houses to delete. {idCasa=}")
