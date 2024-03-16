import calendar
import os
from datetime import datetime, timedelta
import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import load_dotenv
from .day import clinic_day
from ..models.timeslot import slot_helper

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
timeslot_collection = database.get_collection("timeslot")


# async def get_timeslot(date: str, clinic: str):
#     timeslot_collection = db.get_collection(date)
#     slots = []
#     async for s in timeslot_collection.find({"date": date, "clinic_id": clinic}):
#         slots.append(slot_helper(s))
#     return slots

async def get_timeslot(date: str, clinic: str):
    slots = []
    async for s in timeslot_collection.find({"date": date, "clinic_id": clinic}):
        slots.append(slot_helper(s))
    return slots


class Timeslot(dict):
    def add(self, key, value):
        self[key] = value


async def find_day(date):
    day = datetime.strptime(date, '%Y-%m-%d').weekday()
    return calendar.day_name[day]


# async def create_timeslot(date: str, clinic: str):
#     slots = []
#     day = await find_day(date)
#     timeslot_collection = db.get_collection(date)
#     data = await clinic_day(clinic, day)
#     start_time = data.get('start')
#     end_time = data.get('end')
#     gap = data.get('gap')
#     start = datetime.strptime(start_time, '%H:%M')
#     end = datetime.strptime(end_time, '%H:%M') - timedelta(minutes=gap)
#     while start <= end:
#         data = Timeslot()
#         data.add("timeslot", start.strftime("%H:%M"))
#         data.add("date", date)
#         data.add("day", day)
#         data.add("clinic_id", clinic)
#         data.add("status", 0)
#         await timeslot_collection.insert_one(data)
#         slots.append(slot_helper(data))
#         start += timedelta(minutes=gap)
#     return slots

async def create_timeslot(date: str, clinic: str):
    slots = []
    day = await find_day(date)
    data = await clinic_day(clinic, day)
    start_time = data.get('start')
    end_time = data.get('end')
    gap = data.get('gap')
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M') - timedelta(minutes=gap)
    while start <= end:
        data = Timeslot()
        data.add("timeslot", start.strftime("%H:%M"))
        data.add("date", date)
        data.add("day", day)
        data.add("clinic_id", clinic)
        data.add("status", 0)
        await timeslot_collection.insert_one(data)
        slots.append(slot_helper(data))
        start += timedelta(minutes=gap)
    return slots


# async def list_timeslot(date: str, clinic: str):
#     index = await get_timeslot(date, clinic)
#     if len(index) == 0:
#         new_index = await create_timeslot(date, clinic)
#         return new_index
#     return index
#
#
# async def update_timeslot_to_booked(id: str, date: str):
#     timeslot_collection = db.get_collection(date)
#     slot = await timeslot_collection.find_one({"_id": ObjectId(id)})
#     if slot:
#         data = {"status": 1}
#         updated = await timeslot_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
#         if updated:
#             return True
#
#
# async def update_timeslot_to_available(id: str, date: str):
#     timeslot_collection = db.get_collection(date)
#     slot = await timeslot_collection.find_one({"_id": ObjectId(id)})
#     if slot:
#         data = {"status": 0}
#         updated = await timeslot_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
#         if updated:
#             return True

async def list_timeslot(date: str, clinic: str):
    index = await get_timeslot(date, clinic)
    if len(index) == 0:
        new_index = await create_timeslot(date, clinic)
        return new_index
    return index


async def update_timeslot_to_booked(id: str, date: str):
    slot = await timeslot_collection.find_one({"_id": ObjectId(id), "date": date})
    if slot:
        data = {"status": 1}
        updated = await timeslot_collection.update_one({"_id": ObjectId(id), "date": date}, {"$set": data})
        if updated:
            return True


async def update_timeslot_to_available(id: str, date: str):
    slot = await timeslot_collection.find_one({"_id": ObjectId(id), "date": date})
    if slot:
        data = {"status": 0}
        updated = await timeslot_collection.update_one({"_id": ObjectId(id), "date": date}, {"$set": data})
        if updated:
            return True
