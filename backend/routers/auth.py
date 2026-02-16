from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from core.exceptions import AppException
from core.security import create_access_token, verify_password
from db.models import User
from db.session import get_db
from schemas.auth import LoginRequest

# ログイン関連 API（/auth）
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    メールとパスワードで認証し、JWT アクセストークンを返す。
    失敗時は 401 とし、ユーザー不在とパスワード不一致は同じメッセージで返す（列挙攻撃対策）。
    """
    # メールでユーザーを1件取得（削除済みは除外）
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .filter(User.deleted_flag == False)
        .first()
    )

    if not user:
        raise AppException(
            status_code=401,
            error_code="USER_NOT_FOUND",
            message="ユーザーが存在しません",
        )

    # 平文パスワードとDBのハッシュを照合
    if not verify_password(login_data.password, user.password):
        raise AppException(
            status_code=401,
            error_code="USER_NOT_FOUND",
            message="メールアドレスまたはパスワードが正しくありません",
        )

    # JWT に sub（ユーザーID）と role を入れ、アクセストークンを発行
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    """ログイン中ユーザーの情報を返す。"""
    return {"user_id": current_user.id, "email": current_user.email, "role": current_user.role}
