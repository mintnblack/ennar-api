import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import load_dotenv
from ..models.day import day_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
day_collection = database.get_collection("day")


async def add_day(data: dict) -> dict:
    day = await day_collection.insert_one(data)
    new_day = await day_collection.find_one({"_id": day.inserted_id})
    return day_helper(new_day)


async def delete_day(id: str):
    day = await day_collection.find_one({"_id": ObjectId(id)})
    if day:
        await day_collection.delete_one({"_id": ObjectId(id)})
    return True


async def delete_all_clinic_days(clinic: str):
    day = await day_collection.delete_many({"clinic_id": clinic})
    if day:
        return True


async def retrieve_day(id: str):
    day = await day_collection.find_one({"_id": ObjectId(id)})
    if day:
        return day_helper(day)


async def retrieve_days(clinic: str):
    days = []
    async for day in day_collection.find({"clinic_id": clinic}):
        days.append(day_helper(day))
    return days


# async def retrieve_clinics_by_day(day: str):
#     days = []
#     async for day in day_collection.find({"day": day}):
#         days.append(day_helper(day))
#     return days


async def clinic_day(clinic: str, day: str):
    data = await day_collection.find_one({"clinic_id": clinic, "day": day})
    if data:
        return day_helper(data)
