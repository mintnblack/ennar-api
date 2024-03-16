from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from ..utils import timezone as tz


class BlogSchema(BaseModel):
    title: str = Field(...)
    author: str = Field(...)
    image_path: str = Field(...)
    image_tag: str = Field(...)
    html: str = Field(...)
    category_id: str = Field(...)
    category_name: str = Field(...)
    featured: bool = Field(default=False)
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdateBlogSchema(BaseModel):
    title: str = Field(default=None)
    author: str = Field(default=None)
    image_path: str = Field(default=None)
    image_tag: str = Field(default=None)
    html: str = Field(default=None)
    featured: bool = Field(default=None)
    updated: datetime = Field(default=datetime.now().astimezone(tz))


def blog_helper(blog) -> dict:
    return {
        "id": str(blog["_id"]),
        "category_id": blog["category_id"],
        "category_name": blog["category_name"],
        "title": blog["title"],
        "author": blog["author"],
        "image_path": blog["image_path"],
        "image_tag": blog["image_tag"],
        "html": blog["html"],
        "featured": blog["featured"],
        "created": blog["created"],
        "updated": blog["updated"]
    }