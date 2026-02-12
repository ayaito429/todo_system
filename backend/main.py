from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.handlers import register_exception_handlers
from db.base import Base
from db.session import engine
from db import models
from routers.tasks import router as tasks_router

app = FastAPI()
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)


@app.get("/")
def health_check():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}
