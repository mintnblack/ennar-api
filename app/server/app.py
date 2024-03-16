from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .routes.callback import router as callback_router

from .routes.feedback import router as feedback_router

from .routes.category import router as category_router

from .routes.blog import router as blog_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# checking app status
@app.get("/", tags=["API Health"])
async def read_root():
    return {"message": "Hi Dev, Welcome to Ennar API! I'm up and running healthy"}


# define routers
app.include_router(callback_router, tags=["callback"], prefix="/callback")

app.include_router(feedback_router, tags=["feedback"], prefix="/feedback")

app.include_router(category_router, tags=["category"], prefix="/category")

app.include_router(blog_router, tags=["blog"], prefix="/blog")
