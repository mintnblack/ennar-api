from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from typing import List
from ..databases.callback import (
    add_callback,
    update_callback,
    delete_callback,
    bulk_delete_callback,
    retrieve_callbacks,
    retrieve_pending,
    retrieve_completed,
    retrieve_callback
)
from ..models.callback import CallbackSchema, UpdateCallbackSchema
from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="callback added")
async def add_callback_(data: CallbackSchema = Body(...)):
    callback = jsonable_encoder(data)
    new_callback = await add_callback(callback)
    return ResponseModel(new_callback, "callback added")


@router.get("/", response_description="callbacks retrieved")
async def retrieve_callbacks_():
    callbacks = await retrieve_callbacks()
    if callbacks:
        return ListResponseModel(callbacks, "callbacks retrieved")
    return ListResponseModel(callbacks, "empty list")


@router.get("/pending/", response_description="callbacks retrieved")
async def retrieve_pending_():
    callbacks = await retrieve_pending()
    if callbacks:
        return ListResponseModel(callbacks, "callbacks retrieved")
    return ListResponseModel(callbacks, "empty list")


@router.get("/completed/", response_description="callbacks retrieved")
async def retrieve_completed_():
    callbacks = await retrieve_completed()
    if callbacks:
        return ListResponseModel(callbacks, "callbacks retrieved")
    return ListResponseModel(callbacks, "empty list")


@router.get("/{id}/", response_description="callback retrieved")
async def retrieve_callback_(id):
    callback = await retrieve_callback(id)
    if callback:
        return ResponseModel(callback, "success")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/{id}/")
async def update_callback_(id: str, req: UpdateCallbackSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = await update_callback(id, req)
    if updated:
        return ResponseModel("success", "callback updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}/", response_description="callback deleted")
async def delete_callback_(id: str):
    deleted = await delete_callback(id)
    if deleted:
        return ResponseModel("success", "callback deleted")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/bulk/delete/", response_description="callbacks deleted")
async def bulk_delete_callback_(data: List[str]):
    deleted = await bulk_delete_callback(data)
    if deleted:
        return ResponseModel("success", "callbacks deleted")
    return ErrorResponseModel("error", 404, "not found")
