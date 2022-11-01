from pydantic import BaseModel, Field
from typing import List, Optional


class MetaData(BaseModel):
    nombre: str = Field(alias="Nombre")

class Data(BaseModel):
    valor: float = Field(alias="Valor")

class AverageStay(BaseModel):
    nombre: str = Field(alias="Nombre")
    MetaData: List[MetaData] = []
    Data: List[Data] = []

class AverageStayFilter(BaseModel):
    provincia: Optional[str]
    mes: Optional[str]