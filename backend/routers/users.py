# ユーザー関連 API（/api/users）
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from db.models.user import User
from db.session import get_db
from schemas.user import UserCreate, UserResponse
from services import user_service


router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserResponse)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """
    ユーザーを新規作成。
    """
    return user_service.create_user(db=db, user_in=user_in)


@router.get("", response_model=List[UserResponse])
def get_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    ユーザーを取得。
    """
    return user_service.get_user(db=db, login_user=current_user)
