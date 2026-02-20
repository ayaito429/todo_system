from typing import Counter
from sqlalchemy.orm import Session, selectinload


from db.models import Team


def get_team_name(db: Session, team_id: int) -> str:
    """
    idでチーム名を取得
    """
    return (
        db.query(Team.team_name)
        .filter(Team.id == team_id)
        .filter(Team.deleted_flag == False)
        .scalar()
    )


def get_team_and_task(db: Session):
    """
    各チームの全てのタスクを取得
    """

    teams = (
        db.query(Team)
        .options(selectinload(Team.tasks))
        .filter(Team.deleted_flag == False)
        .all()
    )

    result = []
    for team in teams:
        counter = Counter(task.status for task in team.tasks)

        result.append(
            {
                "id": team.id,
                "team_name": team.team_name,
                "status_counts": {
                    "todo": counter.get("未対応", 0),
                    "in_progress": counter.get("対応中", 0),
                    "done": counter.get("完了", 0),
                },
                "all_counts": len(team.tasks),
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "status": task.status,
                        "due_date": task.due_date,
                    }
                    for task in team.tasks
                ],
            }
        )

    return result