# backend/db/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime   
from db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    # タスク名
    title = Column(String, nullable=False)
    # タスクの詳細
    description = Column(String)
    # テータス
    status = Column(String, nullable=False)
    # 優先度
    priority = Column(Integer, nullable=False)
    # 期限日
    due_date = Column(DateTime, nullable=False)
    # 作成日時
    created_at = Column(DateTime, default=datetime.now)
    # 更新日時
    updated_at = Column(DateTime, default=datetime.now)
    # 削除フラグ
    deleted_flag = Column(Boolean, nullable=False)
