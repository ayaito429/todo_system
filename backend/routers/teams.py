from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from services import team_service
from schemas.team import AdminTeams

router = APIRouter(prefix="/api/team", tags=["teams"])


@router.get("/tasks", response_model=List[AdminTeams])
def get_team_tasks(
    db: Session = Depends(get_db),
):
    return team_service.get_team_tasks(db)
