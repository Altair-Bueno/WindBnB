
from typing import Collection, List, Optional
from bson import ObjectId
import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.vivienda import valoracionStateEnum
from app.models.vivienda import NewValoracion, Valoracion
from app.models.vivienda import FilterVivienda
from app.service.error import NotFoundError
from app.models.types import PyObjectId
from app.models.vivienda import viviendaStateEnum
from app.models.vivienda import Vivienda
from app.models.vivienda import NewVivienda, EditVivienda

class ViviendaService:
    collection: AsyncIOMotorCollection

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    '''async def get_viviendas(self) -> List[Vivienda]:
        res = [x async for x in self.collection.find()]
        return res'''
    async def get_viviendas(self, f: FilterVivienda) -> List[Vivienda]:
        pipeline = []

        if f.title:
            pipeline.append({"$match": {"title": {"$regex": f.title}}})
        
        if f.priceMax:
            pipeline.append({"$match": {"price": {"$lte":f.priceMax}}})

        if f.priceMin:
            pipeline.append({"$match": {"price": {"$gte":f.priceMin}}}) 

        return [
            Vivienda(**document)
            async for document in self.collection.aggregate(pipeline)
        ]

    async def new_vivienda(self, request: NewVivienda) -> Vivienda:
        document = request.dict()
        document["state"] = viviendaStateEnum.available.value
        #document["valoraciones"] = []
        
        result = await self.collection.insert_one(document) 
            
        if result.inserted_id:
            return Vivienda(
                id = result.inserted_id,
                **document
            )

    async def get_vivienda_by_id(self, idCasa: PyObjectId) -> Optional[Vivienda]:
        document = await self.collection.find_one(
            {"_id": PyObjectId(idCasa)}
        )
        if document:
            vivienda = document
            return Vivienda(
                id=document["_id"],
                **vivienda
            )
        else:
            raise NotFoundError(

            )

    async def delete_house(self, idCasa: PyObjectId):
        result = await self.collection.update_one(
            {"_id": idCasa},
            {"$set": {
                "state": viviendaStateEnum.deleted.value}}
        )

        if result.modified_count == 0:
            raise NotFoundError(
                f"Couldn't find any available houses to delete. {idCasa=}")

    async def update_house(self, idCasa: PyObjectId, vivienda: EditVivienda):
        result = await self.collection.find_one_and_update(
            {"_id": idCasa},
            {"$set": {
                k:v for k,v in vivienda.dict().items() if v is not None
            }},return_document=pymongo.ReturnDocument.AFTER
        )

        if result:
            return Vivienda(
                    id=result["_id"],
                    **result
                )
        else:
            raise NotFoundError(
                f"Couldn't find any available houses to delete. {idCasa}"
            )

    async def bookings_amount(self, idCasa: PyObjectId):
        result = await self.collection.find_one(
            {"_id": idCasa},
            {"bookings": 1, "_id": 0}
        )
        if result:
            return len(result["bookings"])
        else:
            raise NotFoundError(
                f"Couldn't find any available houses to delete. {idCasa=}"
            )


    async def new_valoracion(self, idCasa: str, valoracion: NewValoracion):
        document = valoracion.dict()
        document["vivienda_id"] = idCasa
        document["state"] = valoracionStateEnum.available.value

        result = await self.collection.insert_one(document)

        if result.inserted_id:
            return Valoracion(
                id = result.inserted_id,
                **document
            )

    async def delete_valoracion(self, idCasa: str, idValoracion: PyObjectId):
        result = await self.collection.update_one(
            {"_id": idValoracion},
            #{"vivienda_id": idCasa},
            {"$set": {
                "state": valoracionStateEnum.deleted.value}}
        )

        if result.modified_count == 0:
            raise NotFoundError(
                f"Couldn't find any available valoration to delete. {idValoracion=}")

    '''async def get_valoraciones(self, idCasa: PyObjectId) -> List[Valoracion]:
        res = [x async for x in self.collection.find({"vivienda_id": idCasa})]
        return res'''
            

