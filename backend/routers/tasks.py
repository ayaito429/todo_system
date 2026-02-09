from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from schemas.task import TaskCreate, TaskResponse, ListTasksQuery
from core.dependencies import get_current_user
from services import task_service

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"]
)


@router.post("", response_model=TaskResponse)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(
        db=db,
        task_in=task_in,
        user_id=current_user.id,
    )


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TaskResponse]:
    return task_service.get_all_tasks(
        db=db,
        user_role=current_user.role,
        team_id=current_user.team_id,
    )
