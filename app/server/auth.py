import os

from datetime import timedelta, datetime

from typing import Annotated

import motor.motor_asyncio

from fastapi import APIRouter, Depends, HTTPException, Body

from starlette import status

from .models.user import user_helper, user_auth_helper

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from jose import jwt, JWTError

from fastapi.encoders import jsonable_encoder

from .models.response import ResponseModel, ErrorResponseModel

from .models.user import UsersSchema, UpdatePasswordSchema, Token

from dotenv import load_dotenv

router = APIRouter()

load_dotenv('.env')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/user/login')

users_collection = database.get_collection('users')
admins_collection = database.get_collection('admins')


async def create_user(data: dict) -> dict:
    new_user = await users_collection.insert_one(data)
    if new_user:
        user_data = await users_collection.find_one({"_id": new_user.inserted_id})
        return user_helper(user_data)


async def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'INVALID CREDENTIALS')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'INVALID USER')


async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({'username': username})
    if not user:
        return False
    user_data = user_auth_helper(user)
    user_password = user_data.get('password')
    if not bcrypt_context.verify(password, user_password):
        return False
    return user_data


async def forgot_password(username: str, password: str, new_password: str):
    authenticated = await authenticate_user(username, password)
    if authenticated:
        pwd = bcrypt_context.hash(new_password)
        updated = await users_collection.update_one({'username': username}, {"$set": {"password": pwd}})
        if updated:
            return True


@router.post("/user/register/", response_description="user added")
async def create_user_(data: UsersSchema = Body(...)):
    user_model = UsersSchema(name=data.name,
                             phone=data.phone,
                             username=data.username,
                             password=bcrypt_context.hash(data.password))
    user = jsonable_encoder(user_model)
    new_user = await create_user(user)
    return ResponseModel(new_user, "success")


@router.post('/user/login/', response_model=Token)
async def access_token_login(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'validation error')
    user_id = user.get('id')
    token = await create_access_token(data.username, user_id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer', 'user_id': user_id}


@router.post("/user/update_password/", response_description="password updated")
async def update_password_(current_user: Annotated[dict, Depends(get_current_user)],
                           data: UpdatePasswordSchema = Body(...)):
    if current_user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    k = await forgot_password(username=data.username,
                              password=data.password,
                              new_password=data.new_password)
    if k:
        return ResponseModel("password Updated", "success")
    return ErrorResponseModel("error", 404, "not found")


@router.get("/current_user/", response_description='current user')
async def current_user_(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return ResponseModel(current_user, "success")
