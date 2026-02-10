from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from db.session import get_db
from db.models.user import User
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


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


@router.put("/{task_id}", response_model=TaskResponse)
def task_update(
    task_id: int,
    update_task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    task = task_service.update_task(db=db, task_id=task_id, update_task=update_task)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
