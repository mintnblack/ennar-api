from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from ..utils import timezone as tz
from ..models.clinic import ClinicSchema
from ..models.user import UsersSchema
from ..models.prescription import PrescriptionSchema


class AppointmentSchema(BaseModel):
    clinic_id: str = Field(...)
    user_id: str = Field(...)
    booking_date: str = Field(...)
    status: int = Field(default=0)
    user: UsersSchema = Field(default=None)
    clinic: ClinicSchema = Field(default=None)
    prescription: PrescriptionSchema = Field(default=None)
    timeslot_id: str = Field(default=None)
    scheduled_date: str = Field(default=None)
    scheduled_slot: str = Field(default=None)
    rejected_reason: int = Field(default=None)
    created: datetime = Field(default=datetime.now().astimezone(tz))
    updated: datetime = Field(default=datetime.now().astimezone(tz))


# for appointment status
# 0 -- pending
# 1 -- scheduled
# 2 -- rejected
# 3 -- rescheduled
# 4 -- unavailabe
# 5 -- completed
# 6 -- canceled

# reject reasons
# 1 -- doctor_unavailable
# 2 -- slots_unavailable
# 3 -- clinic closed
# 4 -- duplicate_appointment
# 5 -- incorrect_information
# 6 -- emergency_cancel
class UpdateAppointmentSchema(BaseModel):
    status: int = Field(...)
    prescription: PrescriptionSchema = Field(default=None)
    timeslot_id:  str = Field(default=None)
    scheduled_date: str = Field(default=None)
    scheduled_slot: str = Field(default=None)
    rejected_reason: str = Field(default=None)
    updated: datetime = Field(default=datetime.now().astimezone(tz))


def appointment_helper(app) -> dict:
    return {
        "id": str(app["_id"]),
        "clinic_id": app["clinic_id"],
        "user_id": app["user_id"],
        "booking_date": app["booking_date"],
        "status": app["status"],
        "user": app["user"],
        "clinic": app["clinic"],
        "prescription": app["prescription"],
        "timeslot_id": app["timeslot_id"],
        "scheduled_date": app["scheduled_date"],
        "scheduled_slot": app["scheduled_slot"],
        "rejected_reason": app["rejected_reason"],
        "created": app["created"],
        'updated': app["updated"]
    }
