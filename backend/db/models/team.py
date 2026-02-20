from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from sqlalchemy.orm import relationship
from db.base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    # チーム名
    team_name = Column(String, nullable=False)
    # 作成日時
    created_at = Column(DateTime, default=datetime.now)
    # 更新日時
    updated_at = Column(DateTime, default=datetime.now)
    # 削除フラグ
    deleted_flag = Column(Boolean, nullable=False)

    # チームID
    tasks = relationship("Task", back_populates="team")
