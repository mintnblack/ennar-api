import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import load_dotenv

from ..models.prescription import prescription_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
prescription_collection = database.get_collection("prescription")


async def retrieve_prescriptions():
    prescriptions = []
    async for prescription in prescription_collection.find().sort("_id", -1):
        prescriptions.append(prescription_helper(prescription))
    return prescriptions


async def add_prescription(prescription_data: dict) -> dict:
    prescription = await prescription_collection.insert_one(prescription_data)
    new_prescription = await prescription_collection.find_one({"_id": prescription.inserted_id})
    return prescription_helper(new_prescription)


async def retrieve_prescription(id: str) -> dict:
    prescription = await prescription_collection.find_one({"_id": ObjectId(id)})
    if prescription:
        return prescription_helper(prescription)


async def update_prescription(id: str, data: dict):
    if len(data) < 1:
        return False
    prescription = await prescription_collection.find_one({"_id": ObjectId(id)})
    if prescription:
        updated = await prescription_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated:
            return True


async def delete_prescription(id: str):
    prescription = await prescription_collection.find_one({"_id": ObjectId(id)})
    if prescription:
        delete = await prescription_collection.delete_one({"_id": ObjectId(id)})
        if delete:
            return True
