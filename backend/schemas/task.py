from typing import List

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime

from schemas.user import UserResponse


class TaskCreate(BaseModel):
    """
    タスク新規作成用（API リクエストボディ）
    """

    # タスク名
    title: str = Field(..., min_length=1, max_length=100)
    # タスクの詳細
    description: str | None = None
    # ステータス
    status: str = Field(...)
    # 優先度
    priority: str = Field(...)
    # 期限日
    due_date: date = Field(...)
    # 担当ユーザーID
    user_id: int = Field(...)
    # チームID
    team_id: int = Field(...)


class TaskResponse(BaseModel):
    """
    タスク情報を返却するレスポンスモデル
    """

    # タスクID
    id: int
    # タイトル
    title: str
    # 詳細
    description: str | None
    # ステータス
    status: str
    # 優先度
    priority: str
    # 期限日
    due_date: date
    # 担当ユーザーID
    user_id: int
    # 担当ユーザー名（未割り当て時は None）
    user_name: str | None
    # チームID
    team_id: int
    # 作成ユーザーID
    created_by: int
    # 作成ユーザー名
    created_name: str
    # 更新ユーザーID
    updated_by: int
    # 更新ユーザー名
    updated_name: str
    # 作成日時
    created_at: datetime
    # 更新日時
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    """
    タスク更新用 リクエストボディ
    """

    # タイトル
    title: str | None = None
    # 詳細
    description: str | None = None
    # 優先度
    priority: str | None = None
    # 期限日
    due_date: date | None = None
    # ステータス
    status: str | None = None
    # 担当ユーザー
    user_id: int | None = None
    # チームID
    team_id: int



class StatusCounts(BaseModel):
    """
    ステータスごとの件数
    """

    # ステータス：未対応
    todo: int
    # ステータス：対応中
    in_progress: int
    # ステータス：完了
    done: int


class TaskInitResponse(BaseModel):
    """
    初期表示 レスポンスモデル
    """

    # タスク一覧
    tasks: List[TaskResponse]
    # チーム名
    team_name: str
    # ステータスごとのタスク件数
    status_counts: StatusCounts
    # タスク総件数
    total_counts: int
    # ユーザー一覧（プルダウン表示用）
    users: List[UserResponse]


class AdminTeamTasks(BaseModel):
    """
    管理者画面 初期表示APIレスポンス
    """

    id: int
    title: str
    status: str
    due_date: Optional[date]
