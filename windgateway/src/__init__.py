from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .beans import get_settings
from .routes import BaseRouter

app = FastAPI()
app.include_router(BaseRouter)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
