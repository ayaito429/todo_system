from sqlalchemy.orm import Session

from repositories import team_repository


def get_team_tasks(db: Session):

    return team_repository.get_team_and_task(db)
