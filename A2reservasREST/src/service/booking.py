from typing import List

import pymongo
from bson.objectid import ObjectId

from src.model.booking import *
from .error import AlreadyBookedError, NotFoundError
from ..model import PyObjectId


class BookingService:
    def __init__(self, collection):
        self.collection = collection

    async def get_booking_by_id(self, booking_id: PyObjectId) -> Optional[Booking]:
        document = await self.collection.find_one({"_id": ObjectId(booking_id)})
        if document:
            return Booking(id=str(document["_id"]), **document)
        else:
            raise NotFoundError()

    async def get_bookings(self, f: FilterBooking) -> List[Booking]:
        query = {}

        if f.user_id:
            query["user_id"] = f.user_id

        if f.before_date:
            query["end_date"] = {"$lte": str(f.before_date)}

        if f.after_date:
            query["start_date"] = {"$gte": str(f.after_date)}

        if f.house_id:
            query["house_id"] = f.house_id

        if f.state:
            query["state"] = f.state.value

        cursor = self.collection.find(query)

        if f.sort_by:
            mode = pymongo.ASCENDING if f.ascending else pymongo.DESCENDING
            cursor.sort(f.sort_by, mode)

        if f.skip:
            cursor.skip(f.skip)

        return [
            Booking(id=str(document["_id"]), **document)
            async for document in cursor.limit(10)
        ]

    async def new_booking(self, request: NewBooking) -> Booking:
        document = {
            "house_id": request.house_id,
            "user_id": request.user_id,
            "start_date": str(request.start_date),
            "end_date": str(request.end_date),
            "state": BookingStateEnum.reserved.value,
        }
        f = {
            "house_id": request.house_id,
            "$or": [
                # Reservations with start date before the given start date
                {
                    "start_date": {"$lte": str(request.start_date)},
                    "end_date": {"$gte": str(request.start_date)},
                },
                # Reservations with end date after the given end date
                {
                    "start_date": {"$lte": str(request.end_date)},
                    "end_date": {"$gte": str(request.end_date)},
                },
                # Reservations smaller than the given reservation
                {
                    "start_date": {"$gte": str(request.start_date)},
                    "end_date": {"$lte": str(request.end_date)},
                },
            ],
        }
        # If nothing matches the filter, the document will be inserted
        result = await self.collection.update_one(
            f,
            {"$setOnInsert": document},
            upsert=True,
        )

        if result.upserted_id:
            return Booking(id=str(result.upserted_id), **request.dict())
        else:
            raise AlreadyBookedError("A booking already exists")

    async def cancel_booking(self, booking_id: PyObjectId):
        result = await self.collection.update_one(
            {"_id": ObjectId(booking_id), "state": BookingStateEnum.reserved.value},
            {"$set": {"state": BookingStateEnum.canceled.value}},
        )

        if result.modified_count == 0:
            raise KeyError(f"Couldn't find any booking with id={booking_id}")
