import os
from datetime import datetime, timedelta
import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi import BackgroundTasks
from dotenv import load_dotenv
import calendar
from ..models.feedback import feedback_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data

feedback_collection = database.get_collection("feedback")


async def add_feedback(data: dict) -> dict:
    feedback = await feedback_collection.insert_one(data)
    new_feedback = await feedback_collection.find_one({"_id": feedback.inserted_id})
    return feedback_helper(new_feedback)


async def update_feedback(id: str, data: dict):
    if len(data) < 1:
        return False
    feedback = await feedback_collection.find_one({"_id": ObjectId(id)})
    if feedback:
        updated = await feedback_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated:
            return True


async def delete_feedback(id: str):
    feedback = await feedback_collection.find_one({"_id": ObjectId(id)})
    if feedback:
        deleted = await feedback_collection.delete_one({"_id": ObjectId(id)})
        if deleted:
            return True
    else:
        return False


async def bulk_delete_feedback(data: list[str]):
    if len(data) < 1:
        return False
    for i in data:
        await delete_feedback(i)
    return True


async def retrieve_feedbacks():
    feedbacks = []
    async for feedback in feedback_collection.find().sort("_id", -1):
        feedbacks.append(feedback_helper(feedback))
    return feedbacks


async def retrieve_approved():
    feedbacks = []
    async for feedback in feedback_collection.find({"status": 1}).sort("_id", -1):
        feedbacks.append(feedback_helper(feedback))
    return feedbacks


async def retrieve_pending():
    feedbacks = []
    async for feedback in feedback_collection.find({"status": 0}).sort("_id", -1):
        feedbacks.append(feedback_helper(feedback))
    return feedbacks


async def retrieve_feedback(id: str) -> dict:
    feedback = await feedback_collection.find_one({"_id": ObjectId(id)})
    if feedback:
        return feedback_helper(feedback)
