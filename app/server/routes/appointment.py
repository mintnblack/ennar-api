from fastapi import APIRouter, Body, BackgroundTasks

from fastapi.encoders import jsonable_encoder

from ..databases.appointment import (
    add_appointment,
    delete_appointment,
    retrieve_appointment,
    retrieve_appointments,
    pending_appointments,
    rejected_appointments,
    canceled_appointments,
    completed_appointments,
    scheduled_appointments,
    rescheduled_appointments,
    unavailable_appointments,
    bulk_delete_appointment,
    search_appointments_by_query_and_date,
    search_appointments_by_date,
    search_appointments_by_query,
    reject_appointment,
    schedule_appointment,
    cancel_pending_appointment,
    cancel_scheduled_appointment,
    reschedule_appointment,
    update_appointment,
    cancel_rescheduled_appointment
)
from ..models.appointment import (
    AppointmentSchema,
    UpdateAppointmentSchema
    # ScheduleAppointmentModel,
    # RejectAppointmentModel,
    # CancelPendingAppointmentModel,
    # CancelScheduledAppointmentModel,
    # UpdateAppointmentModel,
    # RescheduleAppointmentModel,
    # CancelRescheduleAppointmentModel
)
from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="appointment added.")
async def add_appointment_(app: AppointmentSchema = Body(...)):
    appointment = jsonable_encoder(app)
    new_app = await add_appointment(appointment)
    return ResponseModel(new_app, "appointment added")


@router.get("/", response_description="appointments retrieved")
async def retrieve_appointments_():
    appointments = await retrieve_appointments()
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/date/", response_description="appointments retrieved")
async def get_appointments_by_date(first: str, second: str):
    appointments = await search_appointments_by_date(first, second)
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/query/", response_description="appointments retrieved")
async def get_appointments_by_query(query: str):
    appointments = await search_appointments_by_query(query)
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty List")


@router.get("/search/", response_description="appointments retrieved")
async def get_appointments_by_query_and_date(query: str, first: str, second: str):
    appointments = await search_appointments_by_query_and_date(query, first, second)
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty List")


@router.get("/pending/", response_description="appointments retrieved")
async def get_pending_appointments():
    appointments = await pending_appointments()
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/scheduled/", response_description="appointments retrieved")
async def get_scheduled_appointments():
    appointments = await scheduled_appointments()
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/rejected/", response_description="appointments retrieved")
async def get_rejected_appointments():
    appointments = await rejected_appointments()
    if appointments:
        return ListResponseModel(appointments, "Appointments retrieved")
    return ListResponseModel(appointments, "Empty list")


@router.get("/canceled/", response_description="appointments retrieved")
async def get_cancelled_appointments():
    appointments = await canceled_appointments()
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/completed/", response_description="appointments retrieved")
async def get_completed_appointments():
    appointments = await completed_appointments()
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/rescheduled/", response_description="appointments retrieved")
async def get_rescheduled_appointments():
    appointments = await rescheduled_appointments()
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/unavailable/", response_description="appointments retrieved")
async def get_unavailable_appointments():
    appointments = await unavailable_appointments()
    if appointments:
        return ListResponseModel(appointments, "appointments retrieved")
    return ListResponseModel(appointments, "empty list")


@router.get("/{id}/", response_description="appointment retrieved")
async def get_appointment(id):
    app = await retrieve_appointment(id)
    if app:
        return ResponseModel(app, "appointment retrieved")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/pending/schedule/{id}/")
async def schedule_appointment_(bg: BackgroundTasks, id: str, req: UpdateAppointmentSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_appointment = await schedule_appointment(id, req, bg)
    if updated_appointment:
        return ResponseModel("success", "appointment scheduled")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/pending/reject/{id}/")
async def reject_appointment_(bg: BackgroundTasks, id: str, req: UpdateAppointmentSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_appointment = await reject_appointment(id, req, bg)
    if updated_appointment:
        return ResponseModel("success", "appointment rejected")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/pending/cancel/{id}/")
async def cancel_pending_appointment_(bg: BackgroundTasks, id: str, req: UpdateAppointmentSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_appointment = await cancel_pending_appointment(id, req, bg)
    if updated_appointment:
        return ResponseModel("success", "appointment canceled")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/scheduled/cancel/{id}/")
async def cancel_scheduled_appointment_(bg: BackgroundTasks, id: str, req: UpdateAppointmentSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_appointment = await cancel_scheduled_appointment(id, req, bg)
    if updated_appointment:
        return ResponseModel("success", "appointment canceled")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/rescheduled/cancel/{id}/")
async def cancel_rescheduled_appointment_(bg: BackgroundTasks, id: str, req: UpdateAppointmentSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_appointment = await cancel_rescheduled_appointment(id, req, bg)
    if updated_appointment:
        return ResponseModel("success", "appointment canceled")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/scheduled/reschedule/{id}/")
async def reschedule_appointment_(bg: BackgroundTasks, id: str, req: UpdateAppointmentSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_appointment = await reschedule_appointment(id, req, bg)
    if updated_appointment:
        return ResponseModel("success", "appointment rescheduled")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/update/{id}/")
async def update_appointment_(bg: BackgroundTasks, id: str, req: UpdateAppointmentSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_appointment = await update_appointment(id, req, bg)
    if updated_appointment:
        return ResponseModel("success", "appointment updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}/", response_description="appointment deleted")
async def delete_appointment_(id: str):
    deleted_app = await delete_appointment(id)
    if deleted_app:
        return ResponseModel("success", "appointment deleted")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/bulk_delete/", response_description="appointments deleted")
async def bulk_delete_appointments(id: list[str]):
    deleted_app = await bulk_delete_appointment(id)
    if deleted_app:
        return ResponseModel("success", "appointments deleted")
    return ErrorResponseModel("error", 404, "not found")
