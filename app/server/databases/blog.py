import os
from datetime import datetime, timedelta
import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi import BackgroundTasks
from dotenv import load_dotenv
import calendar
from ..models.blog import blog_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data

blog_collection = database.get_collection("blog")


async def add_blog(data: dict) -> dict:
    blog = await blog_collection.insert_one(data)
    new_blog = await blog_collection.find_one({"_id": blog.inserted_id})
    return blog_helper(new_blog)


async def update_blog(id: str, data: dict):
    if len(data) < 1:
        return False
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog:
        updated = await blog_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated:
            return True


async def delete_blog(id: str):
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog:
        deleted = await blog_collection.delete_one({"_id": ObjectId(id)})
        if deleted:
            return True


async def retrieve_blogs():
    blogs = []
    async for blog in blog_collection.find().sort("_id", -1):
        blogs.append(blog_helper(blog))
    return blogs


async def retrieve_latest_blogs():
    blogs = []
    async for blog in blog_collection.find().sort("_id", -1).limit(3):
        blogs.append(blog_helper(blog))
    return blogs


async def retrieve_blog(id: str) -> dict:
    blog = await blog_collection.find_one({"_id": ObjectId(id)})
    if blog:
        return blog_helper(blog)


async def retrieve_blogs_for_category(category_id: str):
    blogs = []
    async for blog in blog_collection.find({"category_id": category_id}).sort("_id", -1):
        blogs.append(blog_helper(blog))
    return blogs


async def retrieve_featured_blogs():
    blogs = []
    async for blog in blog_collection.find({"featured": True}).sort("_id", -1):
        blogs.append(blog_helper(blog))
    return blogs
