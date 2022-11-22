from typing import List
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
from app.models.vivienda import NewVivienda, EditVivienda
from app.models.vivienda import viviendaStateEnum

from app.models.vivienda import Vivienda
from ..dependencies import get_vivienda_service, get_windbnb_collection

vivienda = APIRouter(tags=["Vivienda"])

NOT_FOUND_RESPONSE = {
    404: {"model": ApiError}
}

"""Get all viviendas"""
@vivienda.get("/viviendas", response_model=List[Vivienda], operation_id="getViviendas")
async def get_viviendas(service: ViviendaService = Depends(get_vivienda_service)):
    return await service.get_viviendas()


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


@vivienda.get("/viviendas/{idCasa}", response_model=Vivienda, operation_id="get_house_by_id", responses=NOT_FOUND_RESPONSE)
async def get_house_by_id(idCasa: PyObjectId, service: ViviendaService = Depends(get_vivienda_service)):
    try:
        return await service.get_vivienda_by_id(idCasa)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.error_code)


@vivienda.put('/viviendas/{idCasa}', response_model=Vivienda, operation_id="update_house", responses=NOT_FOUND_RESPONSE)
async def update_house(idCasa: PyObjectId, vivienda: EditVivienda, service: ViviendaService = Depends(get_vivienda_service)):
    try:  
        return await service.update_house(idCasa, vivienda)   
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=e.error_code
        )


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

@vivienda.get("/viviendas/{idCasa}/getBookingsAmount", response_model=Message, operation_id="bookings amount", responses=NOT_FOUND_RESPONSE)
async def get_house_amount_bookings(idCasa: PyObjectId, service: ViviendaService = Depends(get_vivienda_service)):
    """Gives you the amount of bookings of a house"""
    try:
        num = await service.bookings_amount(idCasa)
        return Message(message=f"This house has {num} bookings")
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=e.error_code
        )