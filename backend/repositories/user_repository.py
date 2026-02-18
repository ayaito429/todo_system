from datetime import datetime, timezone

from sqlalchemy.orm import Session

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
    # 再登録なので論理削除を解除
    existing_user.deleted_flag = False

    # リクエストで受け取った値で上書き
    existing_user.name = new_user.name
    existing_user.email = new_user.email
    existing_user.updated_at = datetime.now(timezone.utc)

    db.add(existing_user)   # セッションに確実に紐づける
    db.commit()
    db.refresh(existing_user)
    return existing_user
