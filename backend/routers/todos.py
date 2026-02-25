# backend/routers/todoRouters.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/todos")
def get_todos():
    return ["task1", "task2"]
