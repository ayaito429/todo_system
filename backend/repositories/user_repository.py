from typing import List
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from services.auth_service import validate_password
from core.security import get_password_hash
from db.models import User


def save(db: Session, user: User) -> User:
    """
    UserエンティティをDBに保存
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def find_by_email(db: Session, email: str) -> User | None:
    """
    emailでユーザーを1件取得。
    存在しない場合は None。
    """
    return db.query(User).filter(User.email == email).first()


def update_for_reregister(db: Session, existing_user: User, new_user: User) -> User:
    """
    論理削除されたユーザーを再登録（復活）させる処理。
    """
    # 再登録なので論理削除を解除
    existing_user.deleted_flag = False

    # リクエストで受け取った値で上書き
    existing_user.name = new_user.name
    existing_user.email = new_user.email
    existing_user.updated_at = datetime.now(timezone.utc)

    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    return existing_user


def change_password_first_time(db: Session, user: User, new_password: str) -> dict:
    """
    初回ログイン時のみ実行されるパスワード変更処理。

    """
    # バリデーションチェック
    validate_password(new_password)
    # パスワードをハッシュ化して保存
    user.password = get_password_hash(new_password)
    # 初回ログインフラグを解除
    user.is_first_login = False
    user.updated_at = datetime.now(timezone.utc)

    # 既存ユーザーを更新対象としてセッションに紐づける
    db.add(user)
    # 変更をDBに反映
    db.commit()
    # DBの最新状態をオブジェクトに反映
    db.refresh(user)

    return {"message": "パスワードを変更しました"}


def get_all_leaders(db: Session) -> List[User]:
    """
    全てのリーダー情報を取得
    """
    return db.query(User).filter(User.role == "leader").order_by(User.name).all()


def get_team_users(db: Session, team_id: int) -> List[User]:
    """
    指定したチームの全てのユーザーを取得
    """
    return (
        db.query(User)
        .filter(User.team_id == team_id)
        .filter(User.role == "user")
        .filter(User.deleted_flag == False)
        .order_by(User.name)
        .all()
    )
