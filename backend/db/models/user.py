# backend/db/models/user.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    # ユーザーID
    id = Column(Integer, primary_key=True)
    # ユーザー名
    name = Column(String, nullable=False)
    # メールアドレス
    email = Column(String, unique=True, nullable=False)
    # パスワード
    password = Column(String, nullable=False)
    # 権限
    role = Column(String, nullable=False)
    # チームID
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    # 作成日時
    created_at = Column(DateTime, default=datetime.now)
    # 更新日時
    updated_at = Column(DateTime, default=datetime.now)
    # 削除フラグ
    deleted_flag = Column(Boolean, nullable=False)

    # 担当タスク（user_id で自分が担当しているタスク）
    assigned_tasks = relationship(
        "Task",
        foreign_keys="Task.user_id",
        back_populates="assigned_user",
    )
    # 作成したタスク（created_by で自分が作成したタスク）
    created_tasks = relationship(
        "Task",
        foreign_keys="Task.created_by",
        back_populates="creator",
    )
