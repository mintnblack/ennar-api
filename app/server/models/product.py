from datetime import datetime

from pydantic import BaseModel, Field

from ..utils import timezone as tz


class ProductSchema(BaseModel):
    name: str = Field(...)
    dosage: str = Field(default=None)
    url: str = Field(...)
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdateProductSchema(BaseModel):
    name: str = Field(default=None)
    dosage: str = Field(default=None)
    url: str = Field(default=None)
    updated: datetime = Field(default=datetime.now().astimezone(tz))


def product_helper(pro) -> dict:
    return {
        "id": str(pro["_id"]),
        "name": pro["name"],
        "dosage": pro["dosage"],
        "url": pro["url"],
        "created": pro["created"],
        'updated': pro["updated"]
    }
