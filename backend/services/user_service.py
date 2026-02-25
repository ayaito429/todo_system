from typing import List
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from core.exceptions import AppException
from db.models import User
from repositories import user_repository
from schemas.user import UserCreate, UserResponse
from core.security import get_password_hash


def create_user(db: Session, user_in: UserCreate) -> UserResponse:
    """
    ユーザー新規作成。
    """

    # 既に登録されているユーザーか確認
    existing = user_repository.find_by_email(db, user_in.email)

    if existing:
        if existing.deleted_flag:
            # 再登録（復活＋情報更新）
            user = user_repository.update_for_reregister(db, existing, user)
        else:
            raise AppException(
                status_code=409,
                error_code="EMAIL_ALREADY_REGISTERED",
                message="このメールアドレスは既に登録されています。",
            )
    else:
        # パスワードをハッシュ化
        hashed_password = get_password_hash(user_in.password)
        user = User(
            name=user_in.name,
            email=user_in.email,
            password=hashed_password,
            role=user_in.role,
            team_id=user_in.team_id,
            deleted_flag=False,
            is_first_login=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        user = user_repository.save(db, user)

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        team_id=user.team_id,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def get_user(db: Session, login_user: User) -> List[UserResponse]:
    """
    プルダウンに表示するユーザーを取得
    """

    if login_user.role == "admin":
        users = user_repository.get_all_leaders(db)
    elif login_user.role == "leader":
        users = user_repository.get_team_users(db, login_user.team_id, login_user.id)
    else:
        users = []
    return users
