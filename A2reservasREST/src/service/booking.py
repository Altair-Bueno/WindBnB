from typing import List

import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection

from ..auth import Claims

from .paypal import PaypalService

from .error import *
from ..model import *


class BookingService:
    collection: AsyncIOMotorCollection
    paypal: PaypalService

    def __init__(self, collection: AsyncIOMotorCollection, paypal: PaypalService):
        self.collection = collection
        self.paypal = paypal

    async def get_booking_by_id(self, auth: Claims, booking_id: PyObjectId) -> Optional[Booking]:
        document = await self.collection.find_one(
            {"bookings._id": booking_id},
            {"bookings": {"$elemMatch": {"_id": booking_id, "user_id": auth.sub}}}
        )
        if document:
            booking = document["bookings"][0]
            return Booking(
                house_id=document["_id"],
                id=booking["_id"],
                **booking
            )
        else:
            raise NotFoundError(f"Booking not found. {booking_id=}")

    async def get_bookings(self, auth: Claims, f: FilterBooking) -> List[Booking]:
        pipeline = [
            {"$match": {"bookings.user_id": auth.sub}}
        ]

        if f.house_id:
            pipeline.append({"$match": {"_id": f.house_id}})

        if f.owner_id:
            pipeline.append({"$match": {"user_id": f.owner_id}})

        if f.before_date:
            pipeline.append(
                {"$match": {"bookings.end_date": {"$lte": str(f.before_date)}}})

        if f.after_date:
            pipeline.append({"$match": {
                "bookings.start_date": {"$gte": str(f.after_date)}}})

        if f.state:
            pipeline.append({"$match": {"bookings.state": f.state.value}})

        pipeline.append({"$unwind": "$bookings"})
        pipeline.append({"$project": {
            "id": "$bookings._id",
            "house_id": "$_id",
            "user_id": "$bookings.user_id",
            "start_date": "$bookings.start_date",
            "end_date": "$bookings.end_date",
            "state": "$bookings.state"
        }})

        if f.sort_by:
            pipeline.append({
                "$sort": {
                    f.sort_by: pymongo.ASCENDING if f.ascending else pymongo.DESCENDING}
            })

        pipeline.append({"$skip": f.skip if f.skip else 0})
        pipeline.append({"$limit": 10})

        return [
            Booking(**document)
            async for document in self.collection.aggregate(pipeline)
        ]

    async def new_booking(self, auth: Claims, request: NewBooking) -> PaypalCreateOrderRequestBody:
        booking_id = ObjectId()
        result = await self.collection.update_one(
            {
                "_id": request.house_id,
                "state": HouseStateEnum.available.value,
                "user_id" : {"$ne": auth.sub},
                "bookings": {
                    "$not": {
                        "$elemMatch": {
                            "state": BookingStateEnum.reserved.value,
                            "$or": [
                                {
                                    "start_date": {"$gte": str(request.start_date)},
                                    "end_date": {"$lte": str(request.end_date)},
                                },
                                {
                                    "start_date": {"$lte": str(request.start_date)},
                                    "end_date": {"$gte": str(request.start_date)},
                                }
                            ]
                        }
                    }
                }
            },
            {
                "$push": {
                    "bookings": {
                        "_id": booking_id,
                        "user_id": auth.sub,
                        "state": BookingStateEnum.reserved.value,
                        "start_date": str(request.start_date),
                        "end_date": str(request.end_date),
                    }
                }
            }
        )

        if result.modified_count == 1:
            price_dict = await self.collection.find_one({"_id": request.house_id}, {"price": 1})
            price = price_dict['price']
            time = request.end_date - request.start_date
            value = price * time.days
            return PaypalCreateOrderRequestBody(
                purchase_units=[
                    PaypalPurchaseUnit(amount=PaypalAmount(value=value), invoice_id=str(booking_id))
                ]
            )
        else:
            raise AlreadyBookedError("A booking already exists")

    async def update_booking(self, auth: Claims, booking_id: PyObjectId, order_id: str):
        booking = await self.get_booking_by_id(auth, booking_id)

        order = await self.paypal.capture_order(order_id)
        result = await self.collection.update_one(
            {"bookings._id": booking_id},
            {"$set": {"bookings.$[booking].paypal_order_id": order['id']}},
            array_filters=[{
                "booking._id": booking_id,
                "booking.state": BookingStateEnum.reserved.value,
                "booking.user_id": auth.sub,
                "booking.paypal_transaction_id": None
            }]
        )

        if result.modified_count == 1:
            return await self.get_booking_by_id(auth,booking_id)
        else: 
            raise UpdateBookingError("Couldn't update booking")

    async def cancel_booking(self, auth: Claims, booking_id: PyObjectId):
        result = await self.collection.update_one(
            {"bookings._id": booking_id},
            {"$set": {
                "bookings.$[booking].state": BookingStateEnum.canceled.value}},
            array_filters=[{
                "booking._id": booking_id,
                "booking.user_id": auth.sub,
                "booking.state": BookingStateEnum.reserved.value
            }]
        )

        if result.modified_count == 0:
            raise NotFoundError(
                f"Couldn't find any reserved bookings to cancel. {booking_id=}")
