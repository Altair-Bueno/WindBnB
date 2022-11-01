from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import router
#from services.schedule import rocketry

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
#rocketry.run()