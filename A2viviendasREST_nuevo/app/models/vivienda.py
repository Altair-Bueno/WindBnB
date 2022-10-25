from typing import Optional
from pydantic import BaseModel


class Vivienda(BaseModel):
    title: str
    description: Optional[str]
    user_id: str
    location: str
    state: str