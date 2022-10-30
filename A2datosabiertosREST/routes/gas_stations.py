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


@router.get("/gas-stations/{latitude}/{longitude}")
async def get_stations_by_radius(
        latitude: float,
        longitude: float,
        area: int = Query(default=5),
        limit: int = Query(default=10),
        service: GasStationService = Depends(GasStationService),
):
    return service.find_by_area(area, latitude, longitude, limit)
