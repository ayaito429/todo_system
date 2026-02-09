from pydantic import BaseModel, Field
from datetime import date, datetime

class TaskCreate(BaseModel):
    """タスク新規作成用（API リクエストボディ）"""
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
    # 作成者ユーザーID
    login_user: int = Field(...)

class TaskResponse(BaseModel):
    """
    新規作成したタスク情報を返却するレスポンスモデル
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
    # 作成ユーザーID
    created_by: int
    # 作成日時
    created_at: datetime
    # 更新日時
    updated_at: datetime

    class Config:
        from_attributes = True

class ListTasksQuery(BaseModel):
    """タスク一覧取得時のクエリパラメータ（Postman 検証用：current_user は使わない）"""
    user_role: str
    team_id: int | None = None
