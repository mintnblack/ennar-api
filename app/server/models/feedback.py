from datetime import datetime
from pydantic import BaseModel, Field
from ..utils import timezone as tz


class FeedbackSchema(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phone: str = Field(...)
    treatment: str = Field(...)
    feedback: str = Field(...)
    status: int = Field(default=0)  # 0 -- pending, 1 -- approved
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdateFeedbackSchema(BaseModel):
    status: int = Field(...)
    updated: datetime = Field(default=datetime.now().astimezone(tz))
