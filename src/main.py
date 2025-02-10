from fastapi import FastAPI, APIRouter

from .database import init_db
from .records import router as applications_router

app = FastAPI()

v1_router = APIRouter(prefix="")

v1_router.include_router(applications_router, prefix="")

app.include_router(v1_router)


# Инициализация базы данных
@app.on_event("startup")
async def startup():
    await init_db()
