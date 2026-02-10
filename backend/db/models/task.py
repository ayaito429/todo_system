# backend/db/models/task.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from db.base import Base
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    # タスク名
    title = Column(String, nullable=False)
    # タスクの詳細
    description = Column(String)
    # ステータス
    status = Column(String, nullable=False)
    # 優先度
    priority = Column(String, nullable=False)
    # 期限日
    due_date = Column(DateTime, nullable=False)
    # 担当ユーザーID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 作成者ID
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 作成日時
    created_at = Column(DateTime)
    # 更新日時
    updated_at = Column(DateTime, default=datetime.now)
    # 削除フラグ
    deleted_flag = Column(Boolean, nullable=False)

    # 担当者（user_id に対応）
    assigned_user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="assigned_tasks",
    )
    # 作成者（created_by に対応）
    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_tasks",
    )
