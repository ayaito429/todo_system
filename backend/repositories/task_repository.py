# タスク DB アクセス
from sqlalchemy.orm import Session
from db.models.task import Task


def save(db: Session, task: Task) -> Task:
    """
    TaskエンティティをDBに保存
    """
    db.add(task)
    db.commit()
    db.refresh(task)
    return task