from typing import Optional

from fastapi import APIRouter, Depends

from src.models.average_stay import AverageStayFilter
from src.services.average_stay import AverageStayService

router = APIRouter()


@router.get("/average-stay")
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
