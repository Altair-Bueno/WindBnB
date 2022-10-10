from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from .config import Config

@lru_cache
def MongoClient(config: Config = Depends(Config)):
    # replace this with your MongoDB connection string
    connection_string = config.mongo.url
    # set a 5-second connection timeout
    return AsyncIOMotorClient(connection_string, serverSelectionTimeoutMS=5000)
