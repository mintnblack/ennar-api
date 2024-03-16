from pydantic import BaseModel


class ImageSchema(BaseModel):
    filename: str
    path: str
    tag: str
    content_type: str


def image_helper(res) -> dict:
    return {
        "id": str(res["_id"]),
        "filename": res["filename"],
        "path": res["path"],
        "tag": res["tag"],
        "content_type": res["content_type"]
    }
