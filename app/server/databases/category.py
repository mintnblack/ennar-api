import os
from datetime import datetime, timedelta
import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi import BackgroundTasks
from dotenv import load_dotenv
import calendar

from .blog import retrieve_blogs_for_category
from ..helpers import category_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data

category_collection = database.get_collection("category")


async def add_category(data: dict) -> dict:
    category = await category_collection.insert_one(data)
    new_category = await category_collection.find_one({"_id": category.inserted_id})
    return category_helper(new_category)


async def update_category(id: str, data: dict):
    if len(data) < 1:
        return False
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        updated = await category_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated:
            return True


async def delete_category(id: str):
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        deleted = await category_collection.delete_one({"_id": ObjectId(id)})
        if deleted:
            return True


async def retrieve_categories():
    categories = []
    async for category in category_collection.find().sort("_id", -1):
        categories.append(category_helper(category))
    return categories


async def retrieve_categories_with_blogs():
    categories_with_blogs = []
    categories = await retrieve_categories()
    for category in categories:
        blogs = await retrieve_blogs_for_category(category['id'])
        category.__setitem__('blogs', blogs)
        categories_with_blogs.append(category)
    return categories_with_blogs


async def retrieve_category(id: str) -> dict:
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        return category_helper(category)
