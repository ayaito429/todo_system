from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from schemas.task import TaskCreate, TaskResponse
from core.dependencies import get_current_user
from services import task_service

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"]
)

@router.post("", response_model=TaskResponse)
def create_task_endpoint(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(
        db=db,
        task_in=task_in,
        user_id=current_user.id,
    )
