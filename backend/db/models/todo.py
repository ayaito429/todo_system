from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from db.base import Base


class Todo(Base):

    __tablename__ = "todos"

    # 主キー
    id = Column(Integer, primary_key=True, index=True)
    # タスク名
    title = Column(String, nullable=False)
    # タスクの詳細
    description = Column(String, nullable=True)
    # ステータス（例: "todo" / "doing" / "done"）
    status = Column(String, nullable=False, default="todo")
    # 優先度（1:高, 2:中, 3:低）
    priority = Column(Integer, nullable=False, default=2)
    # 期限日（任意）
    due_date = Column(DateTime, nullable=True)
    # 紐づくユーザー
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 作成日時
    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # 論理削除フラグ
    deleted_flag = Column(Boolean, nullable=False, default=False)
