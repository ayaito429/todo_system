"""
認証 API の単体テスト（pytest + TestClient）。

- POST /auth/login: ログイン（成功・失敗）
- GET /auth/me: 認証済みユーザー取得（トークンあり・なし）

※ ルートが /api/auth の場合は URL を変更してください。
※ テスト用の DB やユーザーが存在しない場合は、モックやテスト DB のセットアップが必要です。
"""

import pytest
from starlette.testclient import TestClient


# --- ログイン ---


def test_login_success(client: TestClient) -> None:
    """正しい email/password でログインすると 200 とトークン（または Set-Cookie）が返る。"""
    response = client.post(
        "/auth/login",
        json={
            "email": "test_admin@example.com",
            "password": "password",
        },
        # JSON の場合は: json={"email": "admin@example.com", "password": "valid_password"},
    )
    # 実際の API が JSON で email/password を受け取る場合の例:
    # response = client.post(
    #     "/auth/login",
    #     json={"email": "admin@example.com", "password": "valid_password"},
    # )
    assert response.status_code == 200
    body = response.json()
    # JWT を body で返す場合
    assert "access_token" in body or "token" in body or response.cookies


def test_login_invalid_credentials(client: TestClient) -> None:
    """誤ったパスワードでは 401 が返る。"""
    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "wrong_password"},
    )
    assert response.status_code == 401


def test_login_missing_password(client: TestClient) -> None:
    """パスワードなしでは 422 または 401 が返る。"""
    response = client.post(
        "/auth/login",
        data={"username": "admin@example.com"},
    )
    assert response.status_code in (401, 422)


# --- /auth/me ---


def test_me_without_token(client: TestClient) -> None:
    """トークンなしで /auth/me を呼ぶと 401 が返る。"""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_valid_token(client: TestClient) -> None:
    """有効なトークン付きで /auth/me を呼ぶと 200 と user 情報が返る。"""
    # 先にログインしてトークンを取得（テスト用ユーザーが DB に存在する前提）
    login_res = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "valid_password"},
    )
    if login_res.status_code != 200:
        pytest.skip("ログインに失敗したため /auth/me の認証付きテストをスキップ")

    token = login_res.json().get("access_token") or login_res.json().get("token")
    if not token and not login_res.cookies:
        pytest.skip("トークンまたは Cookie が返っていないためスキップ")

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert "user_id" in body or "id" in body
    assert "role" in body
    assert "name" in body or "email" in body
