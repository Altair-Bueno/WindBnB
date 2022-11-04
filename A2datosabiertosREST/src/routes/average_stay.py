from typing import Optional

from fastapi import APIRouter, Depends

from src.models.average_stay import AverageStayFilter, Data
from src.models.types import Message
from src.services.average_stay import AverageStayService

router = APIRouter()

NO_DATA_FOUND = {
    418: {"model": Message}
}


@router.get(
    "/average-stay",
    response_model=Data,
    operation_id="get_average_stay",
    responses=NO_DATA_FOUND
)
async def get_average_stay(
        provincia: str,
        mes: Optional[str] = None,
        service: AverageStayService = Depends(AverageStayService),
):
    average_stay_filter = AverageStayFilter(
        provincia=provincia,
        mes=mes
    )
    return await service.find_average_stay(average_stay_filter)
