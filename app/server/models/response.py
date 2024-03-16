def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message
    }


def ListResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
        "count": len(data),
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
