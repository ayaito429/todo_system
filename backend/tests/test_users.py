"""
users ルーター（backend/routers/users.py）の単体テスト。
POST /api/users, GET /api/users をモックで検証する。
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from starlette.testclient import TestClient


def _mock_user_response(
    id: int = 1,
    name: str = "テストユーザー",
    email: str = "test@example.com",
    role: str = "user",
    team_id: int | None = 1,
):
    return {
        "id": id,
        "name": name,
        "email": email,
        "role": role,
        "team_id": team_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


# --- POST /api/users ---


def test_create_user_success(client: TestClient) -> None:
    """ユーザー新規作成が成功すると 200 と UserResponse が返る。"""
    mock_response = _mock_user_response(id=10, name="新規ユーザー", email="new@example.com")
    mock_db = MagicMock()

    def override_get_db():
        yield mock_db

    with patch("routers.users.user_service.create_user", return_value=mock_response):
        from main import app
        from db.session import get_db
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.post(
                "/api/users",
                json={
                    "name": "新規ユーザー",
                    "email": "new@example.com",
                    "role": "user",
                    "password": "password123",
                    "team_id": 1,
                },
            )
            assert response.status_code == 200
            body = response.json()
            assert body["id"] == 10
            assert body["name"] == "新規ユーザー"
            assert body["email"] == "new@example.com"
            assert body["role"] == "user"
            assert "created_at" in body
            assert "updated_at" in body
        finally:
            app.dependency_overrides.pop(get_db, None)


def test_create_user_validation_error(client: TestClient) -> None:
    """必須項目が欠けていると 422 が返る。"""
    response = client.post(
        "/api/users",
        json={
            "name": "のみ",
            # email, role, password, team_id なし
        },
    )
    assert response.status_code == 422


# --- GET /api/users ---


def test_get_users_without_token(client: TestClient) -> None:
    """トークンなしで GET /api/users を呼ぶと 401。"""
    response = client.get("/api/users")
    assert response.status_code == 401


def test_get_users_admin(client: TestClient) -> None:
    """admin で取得すると user_service.get_user が呼ばれ、リーダー一覧が返る。"""
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.role = "admin"
    mock_user.team_id = None
    mock_user.email = "admin@example.com"
    mock_user.name = "管理者"

    mock_list = [
        _mock_user_response(id=2, name="リーダー1", role="leader"),
        _mock_user_response(id=3, name="リーダー2", role="leader"),
    ]
    mock_db = MagicMock()

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.users.user_service.get_user", return_value=mock_list):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get(
                "/api/users",
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 200
            body = response.json()
            assert isinstance(body, list)
            assert len(body) == 2
            assert body[0]["role"] == "leader"
            assert body[1]["name"] == "リーダー2"
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


def test_get_users_leader(client: TestClient) -> None:
    """leader で取得すると自チームのユーザー一覧が返る。"""
    mock_user = MagicMock()
    mock_user.id = 5
    mock_user.role = "leader"
    mock_user.team_id = 1
    mock_user.email = "leader@example.com"
    mock_user.name = "リーダー"

    mock_list = [
        _mock_user_response(id=10, name="メンバー1", role="user", team_id=1),
    ]
    mock_db = MagicMock()

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.users.user_service.get_user", return_value=mock_list):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get(
                "/api/users",
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 200
            body = response.json()
            assert len(body) == 1
            assert body[0]["name"] == "メンバー1"
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)


def test_get_users_normal_user(client: TestClient) -> None:
    """role が user の場合は空リストが返る。"""
    mock_user = MagicMock()
    mock_user.id = 99
    mock_user.role = "user"
    mock_user.team_id = 1
    mock_user.email = "user@example.com"
    mock_user.name = "一般ユーザー"

    mock_db = MagicMock()

    def override_get_current_user():
        return mock_user

    def override_get_db():
        yield mock_db

    with patch("routers.users.user_service.get_user", return_value=[]):
        from main import app
        from core.dependencies import get_current_user
        from db.session import get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get(
                "/api/users",
                headers={"Authorization": "Bearer dummy"},
            )
            assert response.status_code == 200
            assert response.json() == []
        finally:
            app.dependency_overrides.pop(get_current_user, None)
            app.dependency_overrides.pop(get_db, None)
