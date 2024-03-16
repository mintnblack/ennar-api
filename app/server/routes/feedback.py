from fastapi import APIRouter, Body, Depends, status, HTTPException

from typing import Annotated

from fastapi.encoders import jsonable_encoder

from ..auth import get_current_user

from ..databases.feedback import (
    add_feedback,
    update_feedback,
    delete_feedback,
    bulk_delete_feedback,
    retrieve_feedbacks,
    retrieve_pending,
    retrieve_approved,
    retrieve_feedback
)
from ..models.feedback import FeedbackSchema, UpdateFeedbackSchema

from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="feedback added")
async def add_feedback_(current_user: Annotated[dict, Depends(get_current_user)], data: FeedbackSchema = Body(...)):
    if current_user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    feedback = jsonable_encoder(data)
    new_feedback = await add_feedback(feedback)
    return ResponseModel(new_feedback, "feedback added")


@router.get("/", response_description="feedbacks retrieved")
async def retrieve_feedbacks_():
    feedbacks = await retrieve_feedbacks()
    if feedbacks:
        return ListResponseModel(feedbacks, "feedbacks retrieved")
    return ListResponseModel(feedbacks, "empty list")


@router.get("/pending/", response_description="feedbacks retrieved")
async def retrieve_pending_():
    feedbacks = await retrieve_pending()
    if feedbacks:
        return ListResponseModel(feedbacks, "feedbacks retrieved")
    return ListResponseModel(feedbacks, "empty list")


@router.get("/approved/", response_description="feedbacks retrieved")
async def retrieve_approved_():
    feedbacks = await retrieve_approved()
    if feedbacks:
        return ListResponseModel(feedbacks, "feedbacks retrieved")
    return ListResponseModel(feedbacks, "empty list")


@router.get("/{id}/", response_description="feedback retrieved")
async def retrieve_feedback_(id):
    feedback = await retrieve_feedback(id)
    if feedback:
        return ResponseModel(feedback, "success")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/{id}/")
async def update_feedback_(id: str, req: UpdateFeedbackSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = await update_feedback(id, req)
    if updated:
        return ResponseModel("success", "feedback updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}/", response_description="feedback deleted")
async def delete_feedback_(id: str):
    deleted = await delete_feedback(id)
    if deleted:
        return ResponseModel("success", "feedback deleted")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/bulk/", response_description="feedbacks deleted")
async def bulk_delete_feedback_(data: list[str]):
    deleted = await bulk_delete_feedback(data)
    if deleted:
        return ResponseModel("success", "feedbacks deleted")
    return ErrorResponseModel("error", 404, "not found")
