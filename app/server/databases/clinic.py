import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import load_dotenv
from .day import delete_all_clinic_days
from ..models.clinic import clinic_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
clinic_collection = database.get_collection("clinic")


async def retrieve_clinics():
    clinics = []
    async for clinic in clinic_collection.find().sort("_id", -1):
        clinics.append(clinic_helper(clinic))
    return clinics


async def add_clinic(clinic_data: dict) -> dict:
    clinic = await clinic_collection.insert_one(clinic_data)
    new_clinic = await clinic_collection.find_one({"_id": clinic.inserted_id})
    return clinic_helper(new_clinic)


async def retrieve_clinic(id: str) -> dict:
    clinic = await clinic_collection.find_one({"_id": ObjectId(id)})
    if clinic:
        return clinic_helper(clinic)


async def update_clinic(id: str, data: dict):
    if len(data) < 1:
        return False
    clinic = await clinic_collection.find_one({"_id": ObjectId(id)})
    if clinic:
        updated_clinic = await clinic_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_clinic:
            return True


async def delete_clinic(id: str):
    clinic = await clinic_collection.find_one({"_id": ObjectId(id)})
    if clinic:
        delete = await clinic_collection.delete_one({"_id": ObjectId(id)})
        if delete:
            await delete_all_clinic_days(id)
        return True
