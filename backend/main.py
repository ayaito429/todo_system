from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.handlers import register_exception_handlers
from db.base import Base
from db.session import engine
from db import models
from routers.tasks import router as tasks_router
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.teams import router as teams_router

app = FastAPI()
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://13.230.26.135:3000",
        "https://todo-system-ten.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(teams_router)


@app.get("/")
def health_check():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}
