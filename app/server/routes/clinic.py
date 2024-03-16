from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from ..databases.clinic import add_clinic, delete_clinic, retrieve_clinic, retrieve_clinics, update_clinic
from ..models.clinic import ClinicSchema, UpdateClinicModel
from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="clinic added.")
async def add_clinic_(clinic: ClinicSchema = Body(...)):
    clinic = jsonable_encoder(clinic)
    new_clinic = await add_clinic(clinic)
    return ResponseModel(new_clinic, "clinic added.")


@router.get("/", response_description="clinics retrieved")
async def retrieve_clinics_():
    clinics = await retrieve_clinics()
    if clinics:
        return ListResponseModel(clinics, "clinics retrieved")
    return ListResponseModel(clinics, "empty list")


@router.get("/{id}", response_description="clinic retrieved")
async def retrieve_clinic_(id):
    clinic = await retrieve_clinic(id)
    if clinic:
        return ResponseModel(clinic, "clinic retrieved")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/{id}")
async def update_clinic_(id: str, req: UpdateClinicModel = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = await update_clinic(id, req)
    if updated:
        return ResponseModel("success", "clinic updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}", response_description="clinic deleted")
async def delete_clinic_(id: str):
    deleted = await delete_clinic(id)
    if deleted:
        return ResponseModel("success", "clinic deleted")
    return ErrorResponseModel("error", 404, "not found")