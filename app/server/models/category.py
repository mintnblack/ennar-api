from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from ..utils import timezone as tz
from ..models.blog import BlogSchema


class CategorySchema(BaseModel):
    name: str = Field(...)
    blogs: List[BlogSchema] = Field(default=[])
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdateCategorySchema(BaseModel):
    name: str = Field(...)
    updated: datetime = Field(default=datetime.now().astimezone(tz))


def category_helper(cat) -> dict:
    return {
        "id": str(cat["_id"]),
        "name": cat["name"],
        "blogs": cat["blogs"],
        "created": cat["created"],
        "updated": cat["updated"]
    }