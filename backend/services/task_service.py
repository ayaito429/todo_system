from sqlalchemy.orm import Session
from db.models.task import Task
from schemas.task import TaskCreate
from repositories import task_repository
from datetime import datetime

def create_task(db: Session, task_in: TaskCreate, user_id: int) -> Task:
    """
    タスク新規作成
    """

    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
        due_date=task_in.due_date,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_flag=False,
        user_id=user_id,
        created_by=user_id,
    )

    return task_repository.save(db, task)