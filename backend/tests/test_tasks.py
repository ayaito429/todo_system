"""
tasks ルーター（backend/routers/tasks.py）の単体テスト。
POST /api/tasks, GET /api/tasks, PUT /api/tasks/{id}, DELETE /api/tasks/{id} をモックで検証する。
"""
from datetime import date, datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from starlette.testclient import TestClient


def _mock_current_user(id: int = 1, role: str = "user", team_id: int | None = 1):
    u = MagicMock()
    u.id = id
    u.role = role
    u.team_id = team_id
    return u


def _mock_task_response(
    id: int = 1,
    title: str = "タスク1",
    status: str = "未着手",
    user_id: int = 1,
    team_id: int = 1,
):
    return {
        "id": id,
        "title": title,
        "description": "説明",
        "status": status,
        "priority": "高",
        "due_date": date.today().isoformat(),
        "user_id": user_id,
        "team_id": team_id,
        "user_name": "担当者",
        "created_by": 1,
        "created_name": "作成者",
        "updated_by": 1,
        "updated_name": "更新者",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def _mock_task_init_response(tasks_count: int = 2):
    tasks = [_mock_task_response(id=i, title=f"タスク{i}") for i in range(1, tasks_count + 1)]
    return {
        "tasks": tasks,
        "team_name": "テストチーム",
        "status_counts": {"todo": 1, "in_progress": 1, "done": 0},
        "total_counts": len(tasks),
        "users": [
            {"id": 1, "name": "ユーザー1", "email": "u1@example.com", "role": "user", "team_id": 1,
             "created_at": datetime.now(timezone.utc).isoformat(), "updated_at": datetime.now(timezone.utc).isoformat()},
        ],
    }


# --- POST /api/tasks ---


def test_create_task_success(client: TestClient) -> None:
    """認証済みでタスク作成すると 200 と TaskResponse が返る。"""
    mock_user = _mock_current_user(id=5)
    mock_db = MagicMock()
    mock_task = _mock_task_response(id=100, title="新規タスク")

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.tasks.task_service.create_task", return_value=mock_task):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.post(
                "/api/tasks",
                json={
                    "title": "新規タスク",
                    "description": "詳細",
                    "status": "未着手",
                    "priority": "高",
                    "due_date": date.today().isoformat(),
                    "user_id": 1,
                    "team_id": 1,
                },
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 200
            body = response.json()
            assert body["id"] == 100
            assert body["title"] == "新規タスク"
            assert body["status"] == "未着手"
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


def test_create_task_without_token(client: TestClient) -> None:
    """トークンなしでタスク作成すると 401。"""
    response = client.post(
        "/api/tasks",
        json={
            "title": "タスク",
            "status": "未着手",
            "priority": "高",
            "due_date": date.today().isoformat(),
            "user_id": 1,
            "team_id": 1,
        },
    )
    assert response.status_code == 401


def test_create_task_validation_error(client: TestClient) -> None:
    """必須項目不足で 422。"""
    mock_user = _mock_current_user()
    mock_db = MagicMock()

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    from main import app
    from core.dependencies import get_current_user
    from db.session import get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_db] = override_get_db
    try:
        response = client.post(
            "/api/tasks",
            json={"title": ""},  # title のみで他不足
            headers={"Authorization": "Bearer dummy"},
        )
        assert response.status_code == 422
    finally:
        app.dependency_overrides.pop(get_current_user, None)
        app.dependency_overrides.pop(get_db, None)


# --- GET /api/tasks ---


def test_get_tasks_without_token(client: TestClient) -> None:
    """トークンなしで GET /api/tasks は 401。"""
    response = client.get("/api/tasks")
    assert response.status_code == 401


def test_get_tasks_success(client: TestClient) -> None:
    """認証済みで GET /api/tasks すると TaskInitResponse が返る。get_all_tasks は user_role, team_id, login_user_id 付きで呼ばれる。"""
    mock_user = _mock_current_user(id=1, role="user", team_id=1)
    mock_db = MagicMock()
    mock_init = _mock_task_init_response(tasks_count=3)

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.tasks.task_service.get_all_tasks", return_value=mock_init) as m_get_all:
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get("/api/tasks", headers={"Authorization": "Bearer dummy"})
            assert response.status_code == 200
            body = response.json()
            assert "tasks" in body
            assert "team_name" in body
            assert "status_counts" in body
            assert "total_counts" in body
            assert "users" in body
            assert len(body["tasks"]) == 3
            assert body["team_name"] == "テストチーム"
            # get_all_tasks がルーターから user_role, team_id, login_user_id 付きで呼ばれること
            m_get_all.assert_called_once()
            call_kw = m_get_all.call_args[1]
            assert call_kw["user_role"] == "user"
            assert call_kw["team_id"] == 1
            assert call_kw["login_user_id"] == 1
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


# --- PUT /api/tasks/{task_id} ---


def test_update_task_success(client: TestClient) -> None:
    """存在するタスクを更新すると 200 と TaskResponse が返る。"""
    mock_user = _mock_current_user(id=2)
    mock_db = MagicMock()
    mock_task = _mock_task_response(id=50, title="更新後タイトル")

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.tasks.task_service.update_task", return_value=mock_task):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.put(
                "/api/tasks/50",
                json={"title": "更新後タイトル"},
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 200
            assert response.json()["title"] == "更新後タイトル"
            assert response.json()["id"] == 50
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


def test_update_task_not_found(client: TestClient) -> None:
    """存在しないタスクを更新すると 404。"""
    mock_user = _mock_current_user()
    mock_db = MagicMock()

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.tasks.task_service.update_task", return_value=None):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.put(
                "/api/tasks/99999",
                json={"title": "タイトル"},
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 404
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


def test_update_task_without_token(client: TestClient) -> None:
    """トークンなしで更新すると 401。"""
    response = client.put("/api/tasks/1", json={"title": "タイトル"})
    assert response.status_code == 401


# --- DELETE /api/tasks/{task_id} ---


def test_delete_task_success(client: TestClient) -> None:
    """存在するタスクを削除すると 204 が返る。"""
    mock_user = _mock_current_user()
    mock_db = MagicMock()

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.tasks.task_service.delete_task", return_value=True):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.delete(
                "/api/tasks/10",
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 204
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


def test_delete_task_not_found(client: TestClient) -> None:
    """存在しないタスクを削除すると 404。"""
    mock_user = _mock_current_user()
    mock_db = MagicMock()

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.tasks.task_service.delete_task", return_value=False):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.delete(
                "/api/tasks/99999",
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 404
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


def test_delete_task_without_token(client: TestClient) -> None:
    """トークンなしで削除すると 401。"""
    response = client.delete("/api/tasks/1")
    assert response.status_code == 401
