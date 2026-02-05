# backend/config.py
# 環境変数・DB接続設定
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    secret_key: str

    class Config:
        env_file = ".env"  # ローカル用

settings = Settings()

