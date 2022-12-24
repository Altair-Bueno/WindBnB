
from typing import Collection, List, Optional
from bson import ObjectId
import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.vivienda import valoracionStateEnum
from app.models.vivienda import NewValoracion, Valoracion
from app.models.vivienda import FilterVivienda
from app.service.error import NotFoundError
from app.models.types import PyObjectId

class ValoracionService:
    collection: AsyncIOMotorCollection

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

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

    async def get_valoraciones(self, idCasa: PyObjectId) -> List[Valoracion]:
        res = [x async for x in self.collection.find({"vivienda_id": idCasa})]
        return res
            

