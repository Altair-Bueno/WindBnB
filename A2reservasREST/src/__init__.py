from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from .model import Message
from .routes import BaseRouter
from .service.error import *

__name__ = "A2reservasREST"
__version__ = "0.1.0"
__docs__ = "Gestión de reservas. Ingeniería web"


app = FastAPI()
app.include_router(BaseRouter)
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
        title=__name__,
        version=__version__,
        description=__docs__,
        routes=app.routes,
    )

    # Include servers section
    openapi_schema["servers"] = [
        {"url": "/", "description": "Default"},
        {"url": "http://localhost:8001", "description": "Docker compose"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(AlreadyBookedError)
async def already_booked_handler(request, exc):
    return JSONResponse(
        # Conflict
        status_code=409,
        content=Message(message="".join(exc.args)).dict(),
    )


@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        # Not found
        status_code=404,
        content=Message(message="".join(exc.args)).dict(),
    )
