from fastapi import APIRouter, Body

from fastapi.encoders import jsonable_encoder

from ..databases.blog import (
    add_blog,
    update_blog,
    delete_blog,
    retrieve_blogs,
    retrieve_blog,
    retrieve_blogs_for_category,
    retrieve_featured_blogs,
    retrieve_latest_blogs,
)
from ..models.blog import BlogSchema, UpdateBlogSchema

from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="blog added")
async def add_blog_(data: BlogSchema = Body(...)):
    blog = jsonable_encoder(data)
    new_blog = await add_blog(blog)
    return ResponseModel(new_blog, "blog added")


@router.get("/", response_description="blogs retrieved")
async def retrieve_blogs_():
    blogs = await retrieve_blogs()
    if blogs:
        return ListResponseModel(blogs, "blogs retrieved")
    return ListResponseModel(blogs, "empty list")


@router.get("/latest/", response_description="blogs retrieved")
async def retrieve_latest_blogs_():
    blogs = await retrieve_latest_blogs()
    if blogs:
        return ListResponseModel(blogs, "blogs retrieved")
    return ListResponseModel(blogs, "empty list")


@router.get("/category/", response_description="blogs retrieved")
async def retrieve_blogs_for_category_(category_id: str):
    blogs = await retrieve_blogs_for_category(category_id)
    if blogs:
        return ListResponseModel(blogs, "blogs retrieved")
    return ListResponseModel(blogs, "empty list")


@router.get("/featured/", response_description="blogs retrieved")
async def retrieve_featured_blogs_():
    blogs = await retrieve_featured_blogs()
    if blogs:
        return ListResponseModel(blogs, "blogs retrieved")
    return ListResponseModel(blogs, "empty list")


@router.get("/{id}/", response_description="blog retrieved")
async def retrieve_blog_(id):
    blog = await retrieve_blog(id)
    if blog:
        return ResponseModel(blog, "success")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/{id}/")
async def update_blog_(id: str, req: UpdateBlogSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = await update_blog(id, req)
    if updated:
        return ResponseModel("success", "blog updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}/", response_description="blog deleted")
async def delete_blog_(id: str):
    deleted = await delete_blog(id)
    if deleted:
        return ResponseModel("success", "blog deleted")
    return ErrorResponseModel("error", 404, "not found")
