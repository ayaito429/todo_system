from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    POST /auth/login のリクエストボディ。
    メールとパスワードで認証する。
    """

    # ログインに使うメールアドレス（ユーザー一意）
    email: str = Field(...)
    # 平文パスワード（サーバー側でハッシュと照合する）
    password: str = Field(...)
