from enum import Enum
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, PositiveFloat
from app.models.types import PyObjectId
from typing import List


class viviendaStateEnum(str, Enum):
    available = "available"
    deleted = "deleted"

class valoracionStateEnum(str, Enum):
    available = "available"
    deleted = "deleted"

class Valoracion(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    vivienda_id: PyObjectId
    user_id: str
    state: valoracionStateEnum = valoracionStateEnum.available
    valoracion: int
    comentario : str

    class Config:
        json_encoders = {ObjectId: str}

class NewValoracion(BaseModel):
    #vivienda_id: str
    user_id: str
    valoracion: int
    comentario : str

    class Config:
        json_encoders = {ObjectId: str}

class Vivienda(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str]
    user_id: str
    location: str
    state: viviendaStateEnum = viviendaStateEnum.available
    url_photo: Optional[List[str]]
    longitude: str
    latitude: str
    price: PositiveFloat
    #valoraciones : List[PyObjectId]

    class Config:
        json_encoders = {ObjectId: str}


class NewVivienda(BaseModel):
    title: str
    description: Optional[str]
    user_id: str
    location: str
    url_photo: Optional[List[str]]
    longitude: str
    latitude: str
    price: PositiveFloat

    class Config:
        json_encoders = {ObjectId: str}

class EditVivienda(BaseModel):
    title: Optional[str]
    description: Optional[str]
    user_id: Optional[str]
    location: Optional[str]
    url_photo: Optional[List[str]]
    longitude: Optional[str]
    latitude: Optional[str]
    price: Optional[PositiveFloat]
    #valoracion : Optional[PyObjectId]

    class Config:
        json_encoders = {ObjectId: str}

class FilterVivienda(BaseModel):
    title: Optional[str]
    priceMax: Optional[PositiveFloat]
    priceMin: Optional[PositiveFloat]

    class Config:
        json_encoders = {ObjectId: str}

