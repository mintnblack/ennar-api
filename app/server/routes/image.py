import os

import binascii

import motor.motor_asyncio

from bson.objectid import ObjectId

from dotenv import load_dotenv

from fastapi import UploadFile, BackgroundTasks, HTTPException, APIRouter

from starlette.responses import StreamingResponse

from app.server.models.image import image_helper

from app.server.models.response import ResponseModel, ErrorResponseModel

load_dotenv('.env')

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_DETAILS'))
database = client.data
image_collection = database.get_collection('images')
bucket = motor.motor_asyncio.AsyncIOMotorGridFSBucket(database)

router = APIRouter()


async def _generate_hash():
    return binascii.hexlify(os.urandom(16)).decode('utf-8')


async def delete_file(id: str):
    await bucket.delete(id)
    return True


class UploadSchema(dict):
    def add(self, key, value):
        self[key] = value


@router.post('/upload/')
async def upload_image(file: UploadFile):
    filename = file.filename
    ext = filename.split(".")[-1]
    content_type = file.content_type
    if content_type not in ["image/webp",
                            "image/png",
                            "image/svg+xml",
                            "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid File Type")
    try:
        hashed = await _generate_hash()
        tag: str = hashed
        name = hashed + "." + ext
        path = "/image/" + name
        grid_in = bucket.open_upload_stream_with_id(tag, name, metadata={'contentType': content_type})
        data = await file.read()
        await grid_in.write(data)
        await grid_in.close()  # uploaded on close
        img_data = UploadSchema()
        img_data.add("filename", name)
        img_data.add('path', path)
        img_data.add('tag', tag)
        img_data.add('content_type', content_type)
        v = await image_collection.insert_one(img_data)
        k = await image_collection.find_one({'_id': v.inserted_id})
        res = image_helper(k)
        return ResponseModel(res, "image uploaded")
    except ConnectionError as e:
        return HTTPException(408, detail=str(e))


@router.get('/{filename}')
async def stream_image(filename: str):
    image = bucket.find({"filename": filename})
    exists = await image.fetch_next
    if exists:
        grid_out = await bucket.open_download_stream_by_name(filename)

        async def read():
            while grid_out.tell() < grid_out.length:
                yield await grid_out.readchunk()

        media_type = grid_out.metadata.get('contentType')
        return StreamingResponse(read(), status_code=200, media_type=media_type)
    return ErrorResponseModel("error", 404, "not found")


@router.delete('/{tag}')
async def delete_image(tag: str):
    deleted = await delete_file(tag)
    if deleted:
        k = await image_collection.find_one({"tag": tag})
        data = image_helper(k)
        id = data.get("id")
        if k:
            await image_collection.delete_one({"_id": ObjectId(id)})
            return ResponseModel("image deleted", "success")
    return ErrorResponseModel("error", 404, 'not found')
