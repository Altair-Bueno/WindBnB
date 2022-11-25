from fastapi import Depends, FastAPI
from app.routes.vivienda import vivienda
from pymongo import MongoClient
from .dependencies import get_windbnb_collection
from fastapi.openapi.utils import get_openapi

app = FastAPI()

__name__ = "A2viviendasREST"
__version__ = "0.1.0"
__docs__ = "Gestión de viviendas. Ingeniería web"

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=__name__,
        version=__version__,
        description=__docs__,
        routes=app.routes,
    )

    # Include servers section
    openapi_schema["servers"] = [
        {"url": "/", "description": "Default"},
        {"url": "http://localhost:8002", "description": "Docker compose"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(vivienda)
    