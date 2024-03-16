from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from ..utils import timezone as tz


class BlogSchema(BaseModel):
    title: str = Field(...)
    author: str = Field(...)
    image: str = Field(...)
    html: str = Field(...)
    category_id: str = Field(...)
    category_name: str = Field(...)
    featured: bool = Field(default=False)
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdateBlogSchema(BaseModel):
    title: str = Field(default=None)
    author: str = Field(default=None)
    image: str = Field(default=None)
    html: str = Field(default=None)
    featured: bool = Field(default=None)
    updated: datetime = Field(default=datetime.now().astimezone(tz))

