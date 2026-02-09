from sqlalchemy.orm import Session
from db.models.task import Task
from schemas.task import TaskCreate
from repositories import task_repository
from datetime import datetime
from typing import List

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
        deleted_flag=False,
        user_id=task_in.user_id,
        created_by=task_in.login_user,
    )

    return task_repository.save(db, task)

def get_all_tasks(db, user_role, team_id) -> List[Task]:

    if user_role == "admin":
        return task_repository.get_all(db)
    return task_repository.get_by_team(db, team_id)

