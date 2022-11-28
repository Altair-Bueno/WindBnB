from enum import Enum
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, PositiveFloat
from app.models.types import PyObjectId
from typing import List


class viviendaStateEnum(str, Enum):
    available = "available"
    deleted = "deleted"


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

    class Config:
        json_encoders = {ObjectId: str}

class FilterVivienda(BaseModel):
    title: Optional[str]
    priceMax: Optional[PositiveFloat]
    priceMin: Optional[PositiveFloat]

    class Config:
        json_encoders = {ObjectId: str}