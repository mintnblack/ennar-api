def slot_helper(slot) -> dict:
    return {
        "id": str(slot["_id"]),
        "clinic_id": slot["clinic_id"],
        "day": slot["day"],
        "date": slot["date"],
        "timeslot": slot["timeslot"],
        "status": slot["status"],
    }
