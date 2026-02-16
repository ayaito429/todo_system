from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.exceptions import AppException
from core.security import ALGORITHM, SECRET_KEY, oauth2_scheme
from db.session import get_db
from db.models.user import User


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    認証が必要なルートで使用。Authorization: Bearer <token> から JWT を取得し、
    検証して payload の sub でユーザーを DB から取得して返す。失敗時は 401。
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None or not isinstance(user_id, str):
            raise AppException(
                status_code=401,
                error_code="TOKEN_PAYLOAD_INVALID",
                message="トークンにユーザーIDが含まれていません。",
            )
        user_id_int = int(user_id)
    except JWTError:
        raise AppException(
            status_code=401,
            error_code="TOKEN_INVALID",
            message="トークンが無効または期限切れです。再ログインしてください。",
        )
    except ValueError:
        raise AppException(
            status_code=401,
            error_code="TOKEN_PAYLOAD_INVALID",
            message="トークンのユーザーID形式が不正です。",
        )

    # トークン内のユーザーIDで DB から取得（削除済みは除外）
    user = (
        db.query(User)
        .filter(User.id == user_id_int)
        .filter(User.deleted_flag == False)
        .first()
    )

    if user is None:
        raise AppException(
            status_code=401,
            error_code="USER_NOT_FOUND",
            message="ユーザーが存在しません（削除済みの可能性があります）。",
        )

    return user
