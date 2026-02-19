from sqlalchemy.orm import Session

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
