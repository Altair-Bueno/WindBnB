from enum import Enum
from typing import Optional
from pydantic import BaseModel

class viviendaStateEnum(str, Enum):
    available = "available"
    deleted = "deleted"


class Vivienda(BaseModel):
    title: str
    description: Optional[str]
    user_id: str
    location: str
    state: viviendaStateEnum = viviendaStateEnum.available

class NewVivienda(BaseModel):
    title: str
    description: Optional[str]
    user_id: str
    location: str
    