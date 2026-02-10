# タスク DB アクセス
from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from db.models.task import Task
from db.models.user import User
from schemas.task import TaskUpdate
from sqlalchemy.exc import SQLAlchemyError


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

    # None以外の更新項目だけを取り出し、既存タスクに反映
    update_date = update_task.model_dump(exclude_none=True)
    for key, value in update_date.items():
        setattr(task, key, value)

    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task_id: int) -> bool:
    """
    タスクを論理削除する。削除した場合 True、該当が存在しない場合 False。
    """
    task = db.get(Task, task_id)
    if task is None or task.deleted_flag:
        return False

    try:
        task.deleted_flag = True
        task.updated_at = datetime.now(timezone.utc)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise
