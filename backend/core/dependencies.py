from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from fastapi import HTTPException


def get_current_user(db: Session = Depends(get_db)) -> User:
    """認証済みユーザーを返す（開発用: 先頭のユーザーを返すスタブ）"""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="ユーザーが存在しません（初期データを投入してください）")
    return user
