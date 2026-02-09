from fastapi import FastAPI
from db.base import Base
from db.session import engine
from db import models
from routers.tasks import router as tasks_router

app = FastAPI()

app.include_router(tasks_router)


@app.get("/")
def health_check():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}
