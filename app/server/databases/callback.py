import os
from datetime import datetime, timedelta
import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi import BackgroundTasks
from dotenv import load_dotenv
import calendar
from ..models.callback import callback_helper
from typing import List
load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data

callback_collection = database.get_collection("callback")


async def add_callback(data: dict) -> dict:
    callback = await callback_collection.insert_one(data)
    new_callback = await callback_collection.find_one({"_id": callback.inserted_id})
    return callback_helper(new_callback)


async def update_callback(id: str, data: dict):
    if len(data) < 1:
        return False
    callback = await callback_collection.find_one({"_id": ObjectId(id)})
    if callback:
        updated = await callback_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated:
            return True


async def delete_callback(id: str):
    callback = await callback_collection.find_one({"_id": ObjectId(id)})
    if callback:
        deleted = await callback_collection.delete_one({"_id": ObjectId(id)})
        if deleted:
            return True


async def bulk_delete_callback(data: List[str]):
    if len(data) < 1:
        return False
    for i in data:
        await delete_callback(i)
    return True


async def retrieve_callbacks():
    callbacks = []
    async for callback in callback_collection.find().sort("_id", -1):
        callbacks.append(callback_helper(callback))
    return callbacks


async def retrieve_completed():
    callbacks = []
    async for callback in callback_collection.find({"status": 1}).sort("_id", -1):
        callbacks.append(callback_helper(callback))
    return callbacks


async def retrieve_pending():
    callbacks = []
    async for callback in callback_collection.find({"status": 0}).sort("_id", -1):
        callbacks.append(callback_helper(callback))
    return callbacks


async def retrieve_callback(id: str) -> dict:
    callback = await callback_collection.find_one({"_id": ObjectId(id)})
    if callback:
        return callback_helper(callback)
