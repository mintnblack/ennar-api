from datetime import datetime

from typing import List

from pydantic import BaseModel, Field

from ..models.product import ProductSchema

from ..utils import timezone as tz


class PrescriptionSchema(BaseModel):
    notes: str = Field(...)
    products: List[ProductSchema] = Field(...)
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdatePrescriptionSchema(BaseModel):
    notes: str = Field(default=None)
    products: List[ProductSchema] = Field(default=None)
    updated: datetime = Field(default=datetime.now().astimezone(tz))


def prescription_helper(pro) -> dict:
    return {
        "id": str(pro["_id"]),
        "notes": pro["notes"],
        "products": pro["products"],
        "created": pro["created"],
        'updated': pro["updated"]
    }
