# backend/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQLログ出力（開発用）
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
