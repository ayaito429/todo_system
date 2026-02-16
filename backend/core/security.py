# backend/core/security.py
"""
パスワードハッシュと JWT 発行・検証、OAuth2 スキームの定義。
ログイン時は verify_password で照合、create_access_token でトークン発行。
認証が必要なルートでは get_current_user（dependencies）が oauth2_scheme でトークンを受け取る。
"""
from datetime import datetime, timedelta, timezone
import os
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

# Argon2 でパスワードをハッシュ・照合するコンテキスト
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Bearer トークンで Authorization ヘッダーからトークン取得。Swagger のログイン先 URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT の署名に使う秘密鍵とアルゴリズム（本番では環境変数にすること）
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    """平文パスワードを Argon2 でハッシュ化。"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """平文パスワードと DB に保存したハッシュを照合。ログイン時に使用。"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    ペイロードに有効期限 (exp) を付与して JWT を発行。
    data には sub（ユーザーID）や role などを入れる。
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
