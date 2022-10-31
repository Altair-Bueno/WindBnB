from fastapi import APIRouter
from routes import gas_stations, average_stay

router = APIRouter()
router.include_router(gas_stations.router, tags=["Gas Stations"])
router.include_router(average_stay.router, tags=["Average Stay"])
