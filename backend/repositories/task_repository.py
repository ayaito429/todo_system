# タスク DB アクセス
from sqlalchemy.orm import Session
from db.models.task import Task
from db.models.user import User
from typing import List


def save(db: Session, task: Task) -> Task:
    """
    TaskエンティティをDBに保存
    """
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_all(db):
    return (
        db.query(Task)
        .filter(Task.deleted_flag == False)
        .all()
    )

def get_by_team(db, team_id):
    return (
        db.query(Task)
        .join(User, Task.user_id == User.id)
        .filter(User.team_id == team_id)
        .filter(Task.deleted_flag == False)
        .all()
    )
