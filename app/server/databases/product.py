import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import load_dotenv

from ..models.product import product_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
product_collection = database.get_collection("product")


async def retrieve_products():
    products = []
    async for product in product_collection.find().sort("_id", -1):
        products.append(product_helper(product))
    return products


async def add_product(product_data: dict) -> dict:
    product = await product_collection.insert_one(product_data)
    new_product = await product_collection.find_one({"_id": product.inserted_id})
    return product_helper(new_product)


async def retrieve_product(id: str) -> dict:
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)


async def update_product(id: str, data: dict):
    if len(data) < 1:
        return False
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        updated = await product_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated:
            return True


async def delete_product(id: str):
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        delete = await product_collection.delete_one({"_id": ObjectId(id)})
        if delete:
            return True
