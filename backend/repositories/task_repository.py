# タスク DB アクセス
from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session, joinedload

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


def get_by_id(db: Session, task_id: int) -> Task | None:
    """
    IDでタスクを1件取得（assigned_user / creator / updater を joinedload）。
    存在しない場合は None。
    """
    return (
        db.query(Task)
        .options(
            joinedload(Task.assigned_user),
            joinedload(Task.creator),
            joinedload(Task.updater),
        )
        .filter(Task.id == task_id)
        .first()
    )


def get_all(db) -> List[Task]:
    return (
        db.query(Task)
        .options(
            joinedload(Task.assigned_user),
            joinedload(Task.creator),
            joinedload(Task.updater),
        )
        .filter(Task.deleted_flag == False)
        .all()
    )


def get_by_team(db, team_id) -> List[Task]:
    return (
        db.query(Task)
        .options(
            joinedload(Task.assigned_user),
            joinedload(Task.creator),
            joinedload(Task.updater),
        )
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
    task = (
        db.query(Task)
        .options(
            joinedload(Task.assigned_user),
            joinedload(Task.creator),
            joinedload(Task.updater),
        )
        .filter(Task.id == task_id)
        .first()
    )
    if task is None:
        return None

    # None以外の更新項目だけを取り出し、既存タスクに反映
    update_data = update_task.model_dump(exclude_none=True)
    update_data.pop("login_user", None)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.now(timezone.utc)
    if update_task.login_user is not None:
        task.updated_by = update_task.login_user
    db.commit()
    db.refresh(task)
    # レスポンス用にリレーションを再読み込み
    task = (
        db.query(Task)
        .options(
            joinedload(Task.assigned_user),
            joinedload(Task.creator),
            joinedload(Task.updater),
        )
        .filter(Task.id == task_id)
        .first()
    )
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
