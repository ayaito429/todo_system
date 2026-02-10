from sqlalchemy.orm import Session
from db.models.task import Task
from schemas.task import TaskCreate, TaskUpdate
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
        created_at=datetime.now()
    )

    return task_repository.save(db, task)


def get_all_tasks(db, user_role, team_id) -> List[Task]:
    """
    タスク一覧取得
    """
    if user_role == "admin":
        return task_repository.get_all(db)
    return task_repository.get_by_team(db, team_id)


def update_task(db: Session, task_id: int, update_task: TaskUpdate) -> Task | None:
    """
    タスク更新。渡されたフィールドのみ更新（None は変更しない）。
    存在しない task_id の場合は None を返す。
    """
    return task_repository.update(db, task_id, update_task)
