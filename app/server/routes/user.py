from fastapi import APIRouter, Body

from ..databases.user import (
    update_user,
    get_user,
    get_users
)

from ..models.response import (
    ListResponseModel,
    ResponseModel,
    ErrorResponseModel
)

from ..models.user import UpdateUserSchema

router = APIRouter()


@router.get('/', response_description='users retrieved')
async def get_users_():
    users = await get_users()
    if users:
        return ListResponseModel(users, "success")
    return ListResponseModel(users, 'empty list')


@router.get('/{id}', response_description='user retrieved')
async def get_user_(id: str):
    users = await get_user(id)
    if users:
        return ResponseModel(users, 'success')
    return ErrorResponseModel("error", 404, 'not found')


@router.put('/{id}', response_description='user updated')
async def update_user_(id: str, req: UpdateUserSchema = Body(...)):
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel('user updated', "success")
    return ErrorResponseModel("error", 404, 'not found')
