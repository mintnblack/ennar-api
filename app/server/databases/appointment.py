import os

import motor.motor_asyncio

from bson.objectid import ObjectId

from fastapi import BackgroundTasks

from dotenv import load_dotenv

from .timeslot import update_timeslot_to_booked, update_timeslot_to_available

from ..models.appointment import appointment_helper

from ..databases.user import get_user

from ..databases.clinic import retrieve_clinic

from ..databases.prescription import retrieve_prescription

load_dotenv('.env')
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data

appointment_collection = database.get_collection("appointment")


async def retrieve_appointments():
    appointments = []
    async for appointment in appointment_collection.find().sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def search_appointments_by_date(first: str, second: str):
    appointments = []
    async for appointment in appointment_collection.find(
            {"booking_date": {"$gte": first, "$lte": second}}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def search_appointments_by_query(query: str):
    appointments = []
    async for appointment in appointment_collection.find(
            {"$text": {"$search": query}}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def search_appointments_by_query_and_date(query: str, first: str, second: str):
    appointments = []
    async for appointment in appointment_collection.find(
            {"$text": {"$search": query}, "booking_date": {"$gte": first, "$lte": second}}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def pending_appointments():
    appointments = []
    async for appointment in appointment_collection.find(
            {"status": 0}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def scheduled_appointments():
    appointments = []
    async for appointment in appointment_collection.find(
            {"status": 1}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def rejected_appointments():
    appointments = []
    async for appointment in appointment_collection.find(
            {"status": 2}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def canceled_appointments():
    appointments = []
    async for appointment in appointment_collection.find(
            {"status": 6}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def unavailable_appointments():
    appointments = []
    async for appointment in appointment_collection.find(
            {"status": 4}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def rescheduled_appointments():
    appointments = []
    async for appointment in appointment_collection.find(
            {"status": 3}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def completed_appointments():
    appointments = []
    async for appointment in appointment_collection.find(
            {"status": 5}).sort("booking_date", -1):
        appointments.append(appointment_helper(appointment))
    return appointments


async def add_appointment(data: dict) -> dict:
    user_id = data.get('user_id')
    clinic_id = data.get('clinic_id')
    user = await get_user(user_id)
    if user:
        data.__setitem__('user', user)
    clinic = await retrieve_clinic(clinic_id)
    if clinic:
        data.__setitem__('clinic', clinic)
    appointment = await appointment_collection.insert_one(data)
    new_appointment = await appointment_collection.find_one({"_id": appointment.inserted_id})
    return appointment_helper(new_appointment)


async def retrieve_appointment(id: str) -> dict:
    appointment = await appointment_collection.find_one({"_id": ObjectId(id)})
    if appointment:
        return appointment_helper(appointment)


async def delete_appointment(id: str):
    appointment = await appointment_collection.find_one({"_id": ObjectId(id)})
    if appointment:
        await appointment_collection.delete_one({"_id": ObjectId(id)})
    return True


async def bulk_delete_appointment(data: list[str]):
    if len(data) < 1:
        return False
    for i in data:
        await delete_appointment(i)
    return True


async def schedule_appointment(id: str, data: dict, bg: BackgroundTasks):
    if len(data) < 1:
        return False
    slot: str = data.get("timeslot_id")
    date: str = data.get("scheduled_date")
    state: str = data.get("status")
    app = await appointment_collection.find_one({"_id": ObjectId(id)})
    if app:
        updated_app = await appointment_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_app:
            if state == 1:
                bg.add_task(update_timeslot_to_booked, slot, date)
                # send email
                # bg.add_task(appointment_confirmed, data)
            return True


async def reject_appointment(id: str, data: dict, bg: BackgroundTasks):
    if len(data) < 1:
        return False
    state: str = data.get("status")
    reason: str = data.get("rejected_reason")
    app = await appointment_collection.find_one({"_id": ObjectId(id)})
    if app:
        updated_app = await appointment_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_app:
            # if state == 2:
            #     if reason == 1:
            #         bg.add_task(doctor_unavailable, data)
            #     elif reason == 2:
            #         bg.add_task(slots_unavailable, data)
            #     elif reason == 3:
            #         bg.add_task(clinic_closed, data)
            #     elif reason == 4:
            #         bg.add_task(duplicate_appointment, data)
            #     elif reason == 5:
            #         bg.add_task(incorrect_information, data)
            #     elif reason == 6:
            #         bg.add_task(emergency_cancel, data)
            return True


async def cancel_pending_appointment(id: str, data: dict, bg: BackgroundTasks):
    if len(data) < 1:
        return False
    state: str = data.get("status")
    app = await appointment_collection.find_one({"_id": ObjectId(id)})
    if app:
        updated_app = await appointment_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_app:
            # if state == 6:
            #     bg.add_task(pending_canceled, data)
            return True


async def cancel_scheduled_appointment(id: str, data: dict, bg: BackgroundTasks):
    if len(data) < 1:
        return False
    slot: str = data.get("timeslot_id")
    date: str = data.get("scheduled_date")
    state: str = data.get("status")
    app = await appointment_collection.find_one({"_id": ObjectId(id)})
    if app:
        updated_app = await appointment_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_app:
            if state == 6:
                bg.add_task(update_timeslot_to_available, slot, date)
                # send email
                # bg.add_task(scheduled_cancel, data)
            return True


async def cancel_rescheduled_appointment(id: str, data: dict, bg: BackgroundTasks):
    if len(data) < 1:
        return False
    slot: str = data.get("timeslot_id")
    date: str = data.get("scheduled_date")
    state: str = data.get("status")
    app = await appointment_collection.find_one({"_id": ObjectId(id)})
    if app:
        updated_app = await appointment_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_app:
            if state == 6:
                bg.add_task(update_timeslot_to_available, slot, date)
                # send email
                # bg.add_task(rescheduled_cancel, data)
            return True


async def reschedule_appointment(id: str, data: dict, bg: BackgroundTasks):
    if len(data) < 1:
        return False
    state: str = data.get("status")
    slot: str = data.get("timeslot_id")
    date: str = data.get("scheduled_date")
    app = await appointment_collection.find_one({"_id": ObjectId(id)})
    if app:
        updated_app = await appointment_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_app:
            if state == 3:
                bg.add_task(update_timeslot_to_booked, slot, date)
                # send email
                # bg.add_task(rescheduled, data)
            return True


async def update_appointment(id: str, data: dict, bg: BackgroundTasks):
    if len(data) < 1:
        return False
    state: str = data.get("status")
    if state == 5:
        prescription_id = data.get("prescription_id")
        p_data = retrieve_prescription(prescription_id)
        if p_data:
            data.__setitem__('prescription', p_data)
    app = await appointment_collection.find_one({"_id": ObjectId(id)})
    if app:
        updated_app = await appointment_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_app:
            # if state == 5:
            #
            #     send email
            #     bg.add_task(completed, data)
            return True
