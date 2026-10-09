from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from patients import router as patients_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(patients_router)


@app.get("/")
def first_v():
    return {"me":"Hiiiii"}
