from datetime import datetime
from pydantic import BaseModel, Field
from ..utils import timezone as tz


class ClinicSchema(BaseModel):
    name: str = Field(...)
    phone: str = Field(...)
    email: str = Field(...)
    doctor: str = Field(...)
    website: str = Field(...)
    location: str = Field(...)
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


class UpdateClinicModel(BaseModel):
    name: str = Field(default=None)
    phone: str = Field(default=None)
    email: str = Field(default=None)
    doctor: str = Field(default=None)
    website: str = Field(default=None)
    location: str = Field(default=None)
    updated: datetime = Field(default=datetime.now().astimezone(tz))


def clinic_helper(clinic) -> dict:
    return {
        "id": str(clinic["_id"]),
        "name": clinic["name"],
        "phone": clinic["phone"],
        "email": clinic["email"],
        "doctor": clinic["doctor"],
        "website": clinic['website'],
        "location": clinic['location'],
        "created": clinic["created"],
        "updated": clinic["updated"],
    }
