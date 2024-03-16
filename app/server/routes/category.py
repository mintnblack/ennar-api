from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder

from ..databases.category import (
    add_category,
    update_category,
    delete_category,
    retrieve_categories,
    retrieve_category,
    retrieve_categories_with_blogs,
)
from ..models.category import CategorySchema, UpdateCategorySchema

from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="category added")
async def add_category_(data: CategorySchema = Body(...)):
    category = jsonable_encoder(data)
    new_category = await add_category(category)
    return ResponseModel(new_category, "category added")


@router.get("/", response_description="categories retrieved")
async def retrieve_categories_():
    categories = await retrieve_categories()
    if categories:
        return ListResponseModel(categories, "categories retrieved")
    return ListResponseModel(categories, "empty list")


@router.get("/blogs/", response_description="categories retrieved")
async def retrieve_categories_with_blogs_():
    categories = await retrieve_categories_with_blogs()
    if categories:
        return ListResponseModel(categories, "categories retrieved")
    return ListResponseModel(categories, "empty list")


@router.get("/{id}/", response_description="category retrieved")
async def retrieve_category_(id):
    category = await retrieve_category(id)
    if category:
        return ResponseModel(category, "success")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/{id}/")
async def update_category_(id: str, req: UpdateCategorySchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = await update_category(id, req)
    if updated:
        return ResponseModel("success", "category updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}/", response_description="category deleted")
async def delete_category_(id: str):
    deleted = await delete_category(id)
    if deleted:
        return ResponseModel("success", "category deleted")
    return ErrorResponseModel("error", 404, "not found")
