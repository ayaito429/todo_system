"""
teams ルーター（backend/routers/teams.py）の単体テスト。
GET /api/team/tasks をモックで検証する。
"""
from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from starlette.testclient import TestClient


def _mock_admin_teams_list(count: int = 2):
    """AdminTeams 形式のモックリストを返す。"""
    return [
        {
            "id": i,
            "team_name": f"チーム{i}",
            "status_counts": {"todo": 1, "in_progress": 1, "done": 0},
            "all_counts": 2,
            "tasks": [
                {
                    "id": 10 + i,
                    "title": f"タスク{i}-1",
                    "status": "未着手",
                    "due_date": date.today().isoformat(),
                },
                {
                    "id": 20 + i,
                    "title": f"タスク{i}-2",
                    "status": "完了",
                    "due_date": None,
                },
            ],
        }
        for i in range(1, count + 1)
    ]


def test_get_team_tasks_success(client: TestClient) -> None:
    """GET /api/team/tasks で 200 と AdminTeams のリストが返る。"""
    mock_db = MagicMock()
    mock_result = _mock_admin_teams_list(count=2)

    def override_get_db():
        yield mock_db

    with patch("routers.teams.team_service.get_team_tasks", return_value=mock_result):
        from main import app
        from db.session import get_db
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get("/api/team/tasks")
            assert response.status_code == 200
            body = response.json()
            assert isinstance(body, list)
            assert len(body) == 2
            for i, team in enumerate(body):
                assert "id" in team
                assert "team_name" in team
                assert "status_counts" in team
                assert "all_counts" in team
                assert "tasks" in team
                assert team["status_counts"]["todo"] == 1
                assert team["status_counts"]["in_progress"] == 1
                assert team["status_counts"]["done"] == 0
                for task in team["tasks"]:
                    assert "id" in task
                    assert "title" in task
                    assert "status" in task
                    assert "due_date" in task
        finally:
            app.dependency_overrides.pop(get_db, None)


def test_get_team_tasks_empty(client: TestClient) -> None:
    """チームが無い場合は空リストで 200。"""
    mock_db = MagicMock()

    def override_get_db():
        yield mock_db

    with patch("routers.teams.team_service.get_team_tasks", return_value=[]):
        from main import app
        from db.session import get_db
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get("/api/team/tasks")
            assert response.status_code == 200
            assert response.json() == []
        finally:
            app.dependency_overrides.pop(get_db, None)


def test_get_team_tasks_single_team(client: TestClient) -> None:
    """1件のチームのみ返る場合のレスポンス形を検証。"""
    mock_db = MagicMock()
    mock_result = _mock_admin_teams_list(count=1)

    def override_get_db():
        yield mock_db

    with patch("routers.teams.team_service.get_team_tasks", return_value=mock_result):
        from main import app
        from db.session import get_db
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get("/api/team/tasks")
            assert response.status_code == 200
            body = response.json()
            assert len(body) == 1
            assert body[0]["team_name"] == "チーム1"
            assert body[0]["all_counts"] == 2
            assert len(body[0]["tasks"]) == 2
        finally:
            app.dependency_overrides.pop(get_db, None)
