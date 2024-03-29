from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.models.types import Message
from src.routes import router
from src.services.error import NoGasStations, NoDataFound

# from services.schedule import rocketry

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="A2datosabiertosREST Schema",
        version="0.1.0",
        description="Open data service of WindBnB",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# rocketry.run()

@app.exception_handler(NoGasStations)
async def no_gas_stations_handler(request, exc: NoGasStations):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(Message(message="".join(exc.args)).dict())
    )


@app.exception_handler(NoDataFound)
async def no_data_found_handler(request, exc: NoDataFound):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content=jsonable_encoder(Message(message="".join(exc.args)).dict())
    )
