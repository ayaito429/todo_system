from pydantic import BaseModel, Field
from datetime import date, datetime

class TaskCreate(BaseModel):
    """タスク新規作成用（API リクエストボディ）"""
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    status: str = Field(...)
    priority: str = Field(...)
    due_date: date = Field(...)
    user_id: int = Field(...)
    login_user: int = Field(...)

class TaskResponse(BaseModel):
    """
    タスク情報を返却するためのレスポンスモデル
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

    class Config:
        from_attributes = True
