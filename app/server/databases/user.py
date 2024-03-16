import os

import motor.motor_asyncio

from bson import ObjectId

from dotenv import load_dotenv

from ..models.user import user_helper

load_dotenv('.env')

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
users_collection = database.get_collection('users')


async def get_users():
    f = []
    async for k in users_collection.find():
        f.append(user_helper(k))
    return f


async def get_user(id: str) -> dict:
    k = await users_collection.find_one({'_id': ObjectId(id)})
    if k:
        return user_helper(k)


async def get_user_id(username: str):
    k = await users_collection.find_one({'username': username})
    if k:
        v = user_helper(k)
        user_id: str = v.get('id')
        return user_id


async def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    v = await users_collection.find_one({'_id': ObjectId(id)})
    if v:
        k = users_collection.update_one({'_id': ObjectId(id)}, {"$set": data})
        if k:
            return True


async def delete_user(id: str):
    f = await users_collection.find_one({'_id': ObjectId(id)})
    if f:
        await users_collection.delete_one({'_id': ObjectId(id)})
        return True
