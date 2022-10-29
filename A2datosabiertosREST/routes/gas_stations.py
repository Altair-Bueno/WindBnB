from fastapi import APIRouter, Query, Depends
from services.gas_stations import GasStationService

router = APIRouter()


@router.get("/gas-stations/{provincia}")
async def get_gas_stations(
        provincia: str,
        limit: int = Query(default=10),
        service: GasStationService = Depends(GasStationService),
):
    return await service.find_by_provincia(provincia, limit)
