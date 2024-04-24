from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from ..databases.day import add_day, delete_day, retrieve_day, retrieve_days
from ..models.day import DaySchema
from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="Day Added.")
async def add_day_to_clinic(data: DaySchema = Body(...)):
    day = jsonable_encoder(data)
    new_day = await add_day(day)
    return ResponseModel(new_day, "Day Added.")


@router.get("/clinic/{clinic_id}", response_description="days retrieved")
async def retrieve_days_of_clinic(id: str):
    days = await retrieve_days(id)
    if days:
        return ListResponseModel(days, "days retrieved")
    return ListResponseModel(days, "empty list")


# @router.get("/clinics/", response_description="clinics retrieved")
# async def retrieve_clinics_by_day_(day: str):
#     days = await retrieve_clinics_by_day(day)
#     if days:
#         return ListResponseModel(days, "clinics retrieved")
#     return ListResponseModel(days, "empty list")


@router.get("/{id}", response_description="day retrieved")
async def retrieve_day_(id):
    day = await retrieve_day(id)
    if day:
        return ResponseModel(day, "day retrieved ")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}", response_description="day deleted")
async def delete_day_(id: str):
    deleted = await delete_day(id)
    if deleted:
        return ResponseModel("success", "day deleted")
    return ErrorResponseModel("error", 404, "not found")