from bson.objectid import ObjectId
from pydantic import BaseModel


class Message(BaseModel):
    """A single message payload"""

    message: str


class ApiError(BaseModel):
    """An error response"""

    detail: str


class PyObjectId(ObjectId):
    """Wrapper around `pymongo`'s `ObjectId` class for Pydantic"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
