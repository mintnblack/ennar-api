from pydantic import BaseModel, Field


class DaySchema(BaseModel):
    day: str = Field(...)
    start: str = Field(...)
    end: str = Field(...)
    gap: int = Field(...)
    clinic_id: str = Field(...)
    # clinic_name: str = Field(...)


def day_helper(day) -> dict:
    return {
        "id": str(day["_id"]),
        "day": day["day"],
        "start": day["start"],
        "end": day["end"],
        "gap": day["gap"],
        "clinic_id": day["clinic_id"],
        # "clinic_name": day["clinic_name"]
    }
