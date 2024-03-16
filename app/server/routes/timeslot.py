from fastapi import APIRouter
from ..databases.timeslot import list_timeslot
from ..models.response import ListResponseModel

router = APIRouter()


@router.get("/", response_description="timeslots retrieved")
async def retrieve_timeslot(clinic: str, date: str):
    timeslots = await list_timeslot(date=date, clinic=clinic)
    if timeslots:
        return ListResponseModel(timeslots, "timeslots retrieved")
    return ListResponseModel(timeslots, "empty list")
