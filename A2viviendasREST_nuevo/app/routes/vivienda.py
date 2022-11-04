from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from fastapi.responses import Response
from pymongo import ReturnDocument
from app.models.types import PyObjectId
from app.service.error import NotFoundError
from app.models.types import ApiError
from app.models.types import Message
from app.service.vivienda import ViviendaService
from app.models.vivienda import NewVivienda
from app.models.vivienda import viviendaStateEnum

from app.models.vivienda import Vivienda
from ..dependencies import get_vivienda_service, get_windbnb_collection

vivienda = APIRouter()

NOT_FOUND_RESPONSE = {
    404: {"model": ApiError}
}


@vivienda.post("/viviendas", response_model=Vivienda, operation_id="new_house")
async def create_house(request: NewVivienda, service: ViviendaService = Depends(get_vivienda_service)):
    """Creates a new house"""
    #try:
    return await service.new_vivienda(request)
    '''except AlreadyBookedError as e:
        raise HTTPException(
            status_code=409, 
            detail=e.error_code
        )'''

                                                                        

'''@vivienda.get('/viviendas/{idCasa}', response_model=Vivienda)
async def find_house(idCasa: PyObjectId, collection=Depends(get_windbnb_collection)):
    result = await collection.find_one({"_id": ObjectId(idCasa)}, {"_id": 1,
                                                                   "title": 1,
                                                                   "description": 1,
                                                                   "user_id": 1,
                                                                   "location": 1,
                                                                   "state": 1,
                                                                   "url_photo": 1,
                                                                   "longitude": 1,
                                                                   "latitude": 1})
    result["_id"] = str(result["_id"])
    return result'''

@vivienda.get("/viviendas/{idCasa}", response_model=Vivienda, operation_id="get_house_by_id", responses=NOT_FOUND_RESPONSE)
async def get_house_by_id(idCasa: PyObjectId, service: ViviendaService = Depends(get_vivienda_service)):
    try:
        return await service.get_vivienda_by_id(idCasa)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.error_code)


@vivienda.put('/viviendas/{idCasa}', response_model=Vivienda)
async def update_house(idCasa: str, vivienda: Vivienda, collection=Depends(get_windbnb_collection)):
    result = await collection.find_one_and_update({"_id": ObjectId(idCasa)}, {"$set": dict(vivienda)},
                                                  return_document=ReturnDocument.AFTER)
    if result:
        return result
    else:
        return Response(status_code=404)


'''@vivienda.delete('/viviendas/{idCasa}', response_model=Vivienda)
async def delete_house(idCasa: str, collection=Depends(get_windbnb_collection)):
    result = await collection.find_one_and_delete({"_id": ObjectId(idCasa)}) #esto hay que cambiarlo para que se ponga el state a deleted y no se borre de la bd
    if result:
        return Response(status_code=204)
    else:
        return Response(status_code=404)'''

@vivienda.delete("/viviendas/{idCasa}", response_model=Message, operation_id="delete house", responses=NOT_FOUND_RESPONSE)
async def delete_house(idCasa: PyObjectId, service: ViviendaService = Depends(get_vivienda_service)):
    """Cancels the house identified by the given `idCasa`"""
    try: 
        await service.delete_house(idCasa)
        return Message(message=f"Successfully deleted house")
    except NotFoundError as e:
        raise HTTPException(
            status_code=404, 
            detail=e.error_code
        )



