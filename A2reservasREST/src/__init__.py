from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .beans import get_settings
from .model import Message
from .routes import BaseRouter

app = FastAPI()
app.include_router(BaseRouter)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(KeyError)
async def keyerror_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content=Message(message="".join(exc.args)).dict(),
    )
