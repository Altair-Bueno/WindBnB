from fastapi import Depends
from functools import lru_cache
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from .settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


_keys = None


async def get_public_key(settings: Settings = Depends(get_settings)):
    global _keys
    if _keys:
        return _keys

    async with AsyncClient(base_url=settings.auth.baseurl) as client:
        response = await client.get("/.well-known/jwks.json")
        _keys = response.json()["keys"]

    return _keys


@lru_cache
def get_mongo_client(config: Settings = Depends(get_settings)):
    # set a 5-second connection timeout
    return AsyncIOMotorClient(config.mongo.url, serverSelectionTimeoutMS=5000)


@lru_cache
def get_mongo_database(
    client=Depends(get_mongo_client), settings: Settings = Depends(get_settings)
):
    return client[settings.mongo.database]


@lru_cache
def get_windbnb_collection(
    database=Depends(get_mongo_database), settings: Settings = Depends(get_settings)
):
    return database[settings.mongo.collection]


@lru_cache
def get_paypal_service(settings: Settings = Depends(get_settings)):
    from .service import PaypalService

    return PaypalService(settings.paypal)


@lru_cache
def get_booking_service(
    collection=Depends(get_windbnb_collection), paypal=Depends(get_paypal_service)
):
    from .service import BookingService

    return BookingService(collection, paypal)
