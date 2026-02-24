# backend/config.py
# 環境変数・DB接続設定
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int = 5432

    model_config = ConfigDict(env_file=".env")


settings = Settings()
