import datetime
from time import timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.auth_service import validate_password
from repositories import user_repository
from core.dependencies import get_current_user
from core.exceptions import AppException
from core.security import create_access_token, get_password_hash, verify_password
from db.models import User
from db.session import get_db
from schemas.auth import ChangePasswordRequest, LoginRequest

# ログイン関連 API（/auth）
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    メールとパスワードで認証し、JWT アクセストークンを返す。
    失敗時は 401 とし、ユーザー不在とパスワード不一致は同じメッセージで返す（列挙攻撃対策）。
    """
    # メールでユーザーを1件取得
    login_user = user_repository.find_by_email(db, login_data.email)

    # 平文パスワードとDBのハッシュを照合
    if not verify_password(login_data.password, login_user.password):
        raise AppException(
            status_code=401,
            error_code="USER_NOT_FOUND",
            message="メールアドレスまたはパスワードが正しくありません",
        )

    # JWT に sub（ユーザーID）と role を入れ、アクセストークンを発行
    access_token = create_access_token(
        data={
            "sub": str(login_user.id),
            "role": login_user.role,
        }
    )

    return {
        "access_token": access_token,
        "require_password_change": login_user.is_first_login,
    }


@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    """ログイン中ユーザーの情報を返す。"""
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "name": current_user.name,
    }


@router.post("/first-login/password")
def change_password_first_time(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    初回ログイン時はパスワードを変更する
    """

    return user_repository.change_password_first_time(
        db, current_user, payload.new_password
    )
