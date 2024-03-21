from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from ..databases.prescription import add_prescription, delete_prescription, retrieve_prescription, \
    retrieve_prescriptions, update_prescription
from ..models.prescription import PrescriptionSchema, UpdatePrescriptionSchema
from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="prescription added.")
async def add_prescription_(data: PrescriptionSchema = Body(...)):
    prescription = jsonable_encoder(data)
    new_prescription = await add_prescription(prescription)
    return ResponseModel(new_prescription, "prescription added.")


@router.get("/", response_description="prescriptions retrieved")
async def retrieve_prescriptions_():
    prescriptions = await retrieve_prescriptions()
    if prescriptions:
        return ListResponseModel(prescriptions, "prescriptions retrieved")
    return ListResponseModel(prescriptions, "empty list")


@router.get("/{id}", response_description="prescription retrieved")
async def retrieve_prescription_(id):
    prescription = await retrieve_prescription(id)
    if prescription:
        return ResponseModel(prescription, "prescription retrieved")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/{id}")
async def update_prescription_(id: str, req: UpdatePrescriptionSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = await update_prescription(id, req)
    if updated:
        return ResponseModel("success", "prescription updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}", response_description="prescription deleted")
async def delete_prescription_(id: str):
    deleted = await delete_prescription(id)
    if deleted:
        return ResponseModel("success", "prescription deleted")
    return ErrorResponseModel("error", 404, "not found")
