from fastapi import APIRouter
from routes import gas_stations

router = APIRouter()
router.include_router(gas_stations.router, tags=["Gas Stations"])
