from pydantic import BaseModel
from typing import List


class PaypalAmount(BaseModel):
    value: str


class PaypalPurchaseUnit(BaseModel):
    amount: PaypalAmount


class PaypalCreateOrderRequestBody(BaseModel):
    purchase_units: List[PaypalPurchaseUnit]