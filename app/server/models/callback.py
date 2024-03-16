from datetime import datetime
from pydantic import BaseModel, Field
from ..utils import timezone as tz


class CallbackSchema(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phone: int = Field(...)
    message: str = Field(...)
    status: int = Field(default=0)  # 0 -- callback pending, 1 -- callback completed
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdateCallbackSchema(BaseModel):
    status: int = Field()
    updated: datetime = Field(default=datetime.now().astimezone(tz))
