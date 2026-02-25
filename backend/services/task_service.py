from sqlalchemy.orm import Session
from schemas.user import UserResponse
from repositories import team_repository, user_repository
from core.exceptions import AppException
from db.models.task import Task
from schemas.task import (
    StatusCounts,
    TaskCreate,
    TaskInitResponse,
    TaskResponse,
    TaskUpdate,
)
from repositories import task_repository
from datetime import datetime, timezone


def create_task(db: Session, task_in: TaskCreate) -> TaskResponse:
    """
    タスク新規作成。作成者・更新者は task_in.login_user で記録する（ルーターで current_user.id を注入すること）。
    """
    if task_in.login_user is None:
        raise AppException(
            status_code=404, error_code="NOT_FOUND", message="ユーザーが存在しません。"
        )

    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
        due_date=task_in.due_date,
        deleted_flag=False,
        user_id=task_in.user_id,
        team_id=task_in.team_id,
        created_by=task_in.login_user,
        updated_by=task_in.login_user,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    task = task_repository.save(db, task)

    if task is None:
        raise AppException(
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            message="サーバー内部でエラーが発生しました。",
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=task.user_id,
        team_id=task.team_id,
        created_by=task.created_by,
        updated_by=task.updated_by,
        created_at=task.created_at,
        updated_at=task.updated_at,
        user_name=task.assigned_user.name if task.assigned_user else None,
        created_name=task.creator.name if task.creator else None,
        updated_name=task.updater.name if task.updater else None,
    )


def get_all_tasks(
    db: Session, user_role: str, team_id: int | None, login_user_id: int
) -> TaskInitResponse:
    """
    初期表示情報取得
    """
    if user_role == "admin":
        tasks = task_repository.get_all(db)
        users = user_repository.get_all_leaders(db)
    elif team_id is None:
        tasks = []
        users = []
    else:
        tasks = task_repository.get_by_team(db, team_id)
        users = user_repository.get_team_users(db, team_id, login_user_id)

    # タスク一覧
    task_response = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date,
            user_id=task.user_id,
            team_id=task.team_id,
            created_by=task.created_by,
            updated_by=task.updated_by,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_name=task.assigned_user.name if task.assigned_user else None,
            created_name=task.creator.name,
            updated_name=task.updater.name,
        )
        for task in tasks
    ]
    # ユーザー一覧
    user_response = [
        UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            team_id=user.team_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]
    # 各ステータスのタスク件数
    status_counts = task_repository.get_status_counts(db, team_id)
    # ユーザー一覧
    team_name = team_repository.get_team_name(db, team_id)

    return TaskInitResponse(
        tasks=task_response,
        team_name=team_name,
        status_counts=StatusCounts(
            todo=status_counts["todo"],
            in_progress=status_counts["in_progress"],
            done=status_counts["done"],
        ),
        total_counts=len(task_response),
        users=user_response,
    )


def update_task(
    db: Session, task_id: int, update_task: TaskUpdate, updated_by: int
) -> TaskResponse | None:
    """
    タスク更新。渡されたフィールドのみ更新（None は変更しない）。
    存在しない task_id の場合は None を返す。
    """
    update_task_with_user = update_task.model_copy(update={"login_user": updated_by})
    task = task_repository.update(db, task_id, update_task_with_user)
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
