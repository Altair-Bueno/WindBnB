from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr, constr, root_validator, validator
from bson.objectid import ObjectId

from A2reservasREST.src.model import PyObjectId, Booking, HouseStateEnum


class House(BaseModel):
    id: PyObjectId
    title: str
    description: str
    user_id: PyObjectId
    location: str
    state: HouseStateEnum = HouseStateEnum.available
    bookings: [Booking]  # Está bien?

    class Config:
        orm_mode = True


class NewHouse(BaseModel):
    title: str
    description: str
    user_id: PyObjectId
    location: str
    state: HouseStateEnum = HouseStateEnum.available
    bookings = [Booking]

    @validator("title")
    def valid_title(self, title):
        if title.length == 0:
            raise ValueError("House cannot have empty title")

    @validator("description")
    def valid_description(self, desc):
        if desc.length > 500:
            raise ValueError("House description cannot be higher than 500 characters")

    @validator("location")
    def non_empty_location(self, location):
        if location.length == 0:
            raise ValueError("Location cannot be empty")


    class Config:
        json_encoders = {ObjectId: str}


class PostBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreatePostSchema(PostBaseSchema):
    user: ObjectId | None = None
    pass


class PostResponse(PostBaseSchema):
    id: str
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class UpdatePostSchema(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    image: str | None = None
    user: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListPostResponse(BaseModel):
    status: str
    results: int
    posts: List[PostResponse]
