# タスク DB アクセス
from datetime import datetime
from queue import Empty
from typing import List

from sqlalchemy.orm import Session

from db.models.task import Task
from db.models.user import User
from schemas.task import TaskUpdate


def save(db: Session, task: Task) -> Task:
    """
    TaskエンティティをDBに保存
    """
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_all(db) -> List[Task]:
    return db.query(Task).filter(Task.deleted_flag == False).all()


def get_by_team(db, team_id) -> List[Task]:
    return (
        db.query(Task)
        .join(User, Task.user_id == User.id)
        .filter(User.team_id == team_id)
        .filter(Task.deleted_flag == False)
        .all()
    )


def update(db: Session, task_id: int, update_task: TaskUpdate) -> Task | None:
    """
    タスクを更新する。渡されたフィールドのみ上書き（None は無視）。
    存在しない task_id の場合は None を返す。
    """
    task = db.get(Task, task_id)
    if task is None:
        return None

    if update_task.title is not None:
        task.title = update_task.title
    if update_task.description is not None:
        task.description = update_task.description
    if update_task.priority is not None:
        task.priority = update_task.priority
    if update_task.due_date is not None:
        task.due_date = update_task.due_date
    if update_task.status is not None:
        task.status = update_task.status
    if update_task.user_id is not None:
        task.user_id = update_task.user_id

    task.updated_at = datetime.now()
    db.commit()
    db.refresh(task)
    return task
