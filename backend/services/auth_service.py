import re

from core.exceptions import AppException


PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/]{8,}$"
)


def validate_password(password: str) -> None:
    """
    パスワードのバリデーションチェック
    
    """
    if not PASSWORD_REGEX.match(password):
        raise AppException(
            status_code=400,
            error_code="INVALID_PASSWORD_FORMAT",
            message="パスワードは英大文字・英小文字・数字を含む8文字以上で入力してください。",
        )
