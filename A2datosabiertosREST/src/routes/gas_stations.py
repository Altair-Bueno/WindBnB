from typing import Optional

from fastapi import APIRouter, Query, Depends
from src.services.gas_stations import GasStationService
from src.models.gas_stations import EESSPrecioFilter

router = APIRouter()


@router.get("/gas-stations")
async def get_gas_stations(
        provincia: Optional[str] = None,
        rotulo: Optional[str] = None,
        limit: int = Query(default=10),
        service: GasStationService = Depends(GasStationService),
):
    gas_station_filter = EESSPrecioFilter(
        provincia=provincia,
        rotulo=rotulo,
    )
    return await service.find_gas_stations(gas_station_filter, limit)


@router.get("/gas-stations/{latitude}/{longitude}")
async def get_stations_by_radius(
        latitude: float,
        longitude: float,
        area: int = Query(default=5),
        limit: int = Query(default=10),
        service: GasStationService = Depends(GasStationService),
):
    return service.find_by_area(area, latitude, longitude, limit)
