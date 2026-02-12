from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from db.session import get_db
from db.models.user import User
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from services import task_service

# タスク関連 API（/api/tasks）
router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    タスクを新規作成。
    認証済みユーザーのみ実行可能。作成者（created_by / updated_by）は認証ユーザーで固定。
    """
    task_in = task_in.model_copy(update={"login_user": current_user.id})
    return task_service.create_task(db=db, task_in=task_in)


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TaskResponse]:
    """
    タスク一覧を取得。
    admin の場合は全件、それ以外は自チームのタスクのみ返す。認証必須。
    """
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
    """
    指定IDのタスクを更新する（部分更新可。未指定フィールドは変更しない）。
    認証必須。該当タスクが存在しない場合は 404 を返す。
    更新者（updated_by）は認証ユーザーで上書きする（リクエストの login_user は使わない）。
    """
    # 更新者は必ず認証ユーザーにする（クライアント送信値は信頼しない）
    task = task_service.update_task(db=db, task_id=task_id, update_task=update_task, updated_by=current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def task_delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    指定IDのタスクを削除する。認証必須。
    該当タスクが存在しない場合は 404 を返す。成功時は body なし 204。
    """
    deleted = task_service.delete_task(db=db, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
