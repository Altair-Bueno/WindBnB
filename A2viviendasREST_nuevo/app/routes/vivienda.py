from bson import ObjectId
from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from fastapi.responses import Response
from pymongo import ReturnDocument

from app.models.vivienda import Vivienda
from ..dependencies import get_windbnb_collection

vivienda = APIRouter()


@vivienda.post("/viviendas", response_model=Vivienda)
async def create_house(vivienda: Vivienda, collection=Depends(get_windbnb_collection)):
    new_house = dict(vivienda)
    result = await collection.insert_one(new_house)
    return await collection.find_one({"_id": ObjectId(result.inserted_id)}, {"_id": 1,
                                                                             "title": 1,
                                                                             "description": 1,
                                                                             "user_id": 1,
                                                                             "location": 1,
                                                                             "state": 1})


@vivienda.get('/viviendas/{idCasa}', response_model=Vivienda)
async def find_house(idCasa: str, collection=Depends(get_windbnb_collection)):
    result = await collection.find_one({"_id": ObjectId(idCasa)}, {"_id": 1,
                                                                   "title": 1,
                                                                   "description": 1,
                                                                   "user_id": 1,
                                                                   "location": 1,
                                                                   "state": 1})
    result["_id"] = str(result["_id"])
    return result


@vivienda.put('/viviendas/{idCasa}', response_model=Vivienda)
async def update_house(idCasa: str, vivienda: Vivienda, collection=Depends(get_windbnb_collection)):
    result = await collection.find_one_and_update({"_id": ObjectId(idCasa)}, {"$set": dict(vivienda)},
                                                  return_document=ReturnDocument.AFTER)
    if result:
        return result
    else:
        return Response(status_code=404)


@vivienda.delete('/viviendas/{idCasa}', response_model=Vivienda)
async def delete_house(idCasa: str, collection=Depends(get_windbnb_collection)):
    result = await collection.find_one_and_delete({"_id": ObjectId(idCasa)})
    if result:
        return Response(status_code=204)
    else:
        return Response(status_code=404)