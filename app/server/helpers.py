def callback_helper(cb) -> dict:
    return {
        "id": str(cb["_id"]),
        "name": cb["name"],
        "email": cb["email"],
        "phone": cb["phone"],
        "message": cb["message"],
        "status": cb["status"],
        "created": cb["created"],
        "updated": cb["updated"]
    }


def feedback_helper(fb) -> dict:
    return {
        "id": str(fb["_id"]),
        "name": fb["name"],
        "email": fb["email"],
        "phone": fb["phone"],
        "treatment": fb["treatment"],
        "feedback": fb["feedback"],
        "status": fb["status"],
        "created": fb["created"],
        "updated": fb["updated"]
    }


def category_helper(cat) -> dict:
    return {
        "id": str(cat["_id"]),
        "name": cat["name"],
        "blogs": cat["blogs"],
        "created": cat["created"],
        "updated": cat["updated"]
    }


def blog_helper(blog) -> dict:
    return {
        "id": str(blog["_id"]),
        "category_id": blog["category_id"],
        "category_name": blog["category_name"],
        "title": blog["title"],
        "author": blog["author"],
        "image": blog["image"],
        "html": blog["html"],
        "featured": blog["featured"],
        "created": blog["created"],
        "updated": blog["updated"]
    }
