from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """ユーザー新規作成用（API リクエストボディ）"""

    # ユーザー名
    name: str = Field(...)
    # メールアドレス
    email: str = Field(...)
    # 権限
    role: str = Field(...)
    # パスワード
    password: str = Field(...)
    # 所属チーム
    team_id: int = Field(...)


class UserResponse(BaseModel):
    """ユーザー情報を返却するレスポンスモデル"""

    # ユーザーID
    id: int = Field(...)
    # ユーザー名
    name: str = Field(...)
    # メールアドレス
    email: str = Field(...)
    # 権限
    role: str = Field(...)
    # 所属チーム
    team_id: int | None = None
    # 作成日時
    created_at: datetime
    # 更新日時
    updated_at: datetime
