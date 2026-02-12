from sqlalchemy.orm import Session
from db.models.task import Task
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from repositories import task_repository
from datetime import datetime, timezone
from typing import List


def create_task(db: Session, task_in: TaskCreate) -> TaskResponse:
    """
    タスク新規作成。作成者・更新者は task_in.login_user で記録する（ルーターで current_user.id を注入すること）。
    """
    if task_in.login_user is None:
        raise ValueError("login_user is required for create_task")

    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
        due_date=task_in.due_date,
        deleted_flag=False,
        user_id=task_in.user_id,
        created_by=task_in.login_user,
        updated_by=task_in.login_user,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    task = task_repository.save(db, task)
    task = task_repository.get_by_id(db, task.id)
    if task is None:
        raise RuntimeError("Task was saved but could not be reloaded")

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=task.user_id,
        created_by=task.created_by,
        updated_by=task.updated_by,
        created_at=task.created_at,
        updated_at=task.updated_at,
        user_name=task.assigned_user.name if task.assigned_user else None,
        created_name=task.creator.name,
        updated_name=task.updater.name,
    )


def get_all_tasks(db, user_role, team_id) -> List[Task]:
    """
    タスク一覧取得
    """
    if user_role == "admin":
        tasks =  task_repository.get_all(db)
    tasks = task_repository.get_by_team(db, team_id)

    return [
        TaskResponse(
            id = task.id,
            title = task.title,
            description = task.description,
            status = task.status,
            priority = task.priority,
            due_date = task.due_date,
            user_id = task.user_id,
            created_by = task.created_by,
            updated_by = task.updated_by,
            created_at = task.created_at,
            updated_at = task.updated_at,
            user_name=task.assigned_user.name if task.assigned_user else None,
            created_name = task.creator.name,
            updated_name = task.updater.name
        )
        for task in tasks
    ]


def update_task(db: Session, task_id: int, update_task: TaskUpdate, updated_by: int) -> TaskResponse | None:
    """
    タスク更新。渡されたフィールドのみ更新（None は変更しない）。
    存在しない task_id の場合は None を返す。
    """
    task = task_repository.update(db, task_id, update_task)
    if task is None:
        return None

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=task.user_id,
        created_by=task.created_by,
        updated_by=updated_by,
        created_at=task.created_at,
        updated_at=task.updated_at,
        user_name=task.assigned_user.name if task.assigned_user else None,
        created_name=task.creator.name,
        updated_name=task.updater.name,
    )
    
def delete_task(db: Session, task_id: int) -> bool:
    """
    タスクを削除する。削除した場合 True、該当が存在しない場合 False。
    """
    return task_repository.delete(db, task_id)