from fastapi import FastAPI

from .auth import router as auth_router

from .routes.user import router as user_router

from fastapi.middleware.cors import CORSMiddleware

from .routes.callback import router as callback_router

from .routes.feedback import router as feedback_router

from .routes.category import router as category_router

from .routes.blog import router as blog_router

from .routes.image import router as image_router

from .routes.day import router as day_router

from .routes.clinic import router as clinic_router

from .routes.timeslot import router as slot_router

from .routes.product import router as product_router

from .routes.prescription import router as prescription_router

from .routes.appointment import router as appointment_router

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

app.include_router(auth_router, tags=["auth"], prefix="/auth")

app.include_router(user_router, tags=['user'], prefix='/user')

app.include_router(callback_router, tags=["callback"], prefix="/callback")

app.include_router(feedback_router, tags=["feedback"], prefix="/feedback")

app.include_router(category_router, tags=["category"], prefix="/category")

app.include_router(blog_router, tags=["blog"], prefix="/blog")

app.include_router(clinic_router, tags=["clinic"], prefix="/clinic")

app.include_router(day_router, tags=["day"], prefix="/day")

app.include_router(slot_router, tags=["timeslot"], prefix="/timeslot")

app.include_router(image_router, tags=['image'], prefix='/image')

app.include_router(product_router, tags=['product'], prefix='/product')

app.include_router(prescription_router, tags=['prescription'], prefix='/prescription')

app.include_router(appointment_router, tags=['appointment'], prefix='/appointment')
