from typing import List
from pydantic import BaseModel

from schemas.task import AdminTeamTasks, StatusCounts


class AdminTeams(BaseModel):
    """
    管理者画面 初期表示APIレスポンス
    """

    id: int
    team_name: str
    status_counts: StatusCounts
    all_counts: int
    tasks: List[AdminTeamTasks]
