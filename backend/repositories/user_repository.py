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
    emailでタスクを1件取得。
    存在しない場合は None。
    """
    print(db.query(User).filter(User.email == email).first())
    return db.query(User).filter(User.email == email).first()


def update_for_reregister(db: Session, user: User) -> User:
    user.deleted_flag = False
    user.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)
    return user
