from fastapi import Depends, FastAPI
from app.routes.vivienda import vivienda
from pymongo import MongoClient
from .dependencies import get_windbnb_collection


app = FastAPI()

app.include_router(vivienda)

@app.on_event("shutdown")
def shutdown_bd(collection = Depends(get_windbnb_collection)):
    collection.close()
    