from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from ..databases.product import add_product, delete_product, retrieve_product, retrieve_products, update_product
from ..models.product import ProductSchema, UpdateProductSchema
from ..models.response import ResponseModel, ErrorResponseModel, ListResponseModel

router = APIRouter()


@router.post("/", response_description="product added.")
async def add_product_(data: ProductSchema = Body(...)):
    product = jsonable_encoder(data)
    new_product = await add_product(product)
    return ResponseModel(new_product, "product added.")


@router.get("/", response_description="products retrieved")
async def retrieve_products_():
    products = await retrieve_products()
    if products:
        return ListResponseModel(products, "products retrieved")
    return ListResponseModel(products, "empty list")


@router.get("/{id}", response_description="product retrieved")
async def retrieve_product_(id):
    product = await retrieve_product(id)
    if product:
        return ResponseModel(product, "product retrieved")
    return ErrorResponseModel("error", 404, "not found")


@router.put("/{id}")
async def update_product_(id: str, req: UpdateProductSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated = await update_product(id, req)
    if updated:
        return ResponseModel("success", "product updated")
    return ErrorResponseModel("error", 404, "not found")


@router.delete("/{id}", response_description="product deleted")
async def delete_product_(id: str):
    deleted = await delete_product(id)
    if deleted:
        return ResponseModel("success", "product deleted")
    return ErrorResponseModel("error", 404, "not found")