"""
pytest 共通フィクスチャ。
FastAPI の app と TestClient を提供します。

アプリの場所: backend/main.py の app、または backend/app/main.py の app を参照します。
「No module named 'main'」が出る場合は、backend 直下に main.py を用意するか、
アプリが入っているモジュール名に合わせて下記の import を書き換えてください。
"""
import sys
from pathlib import Path

import pytest
from starlette.testclient import TestClient

# プロジェクトルート（backend）をパスに追加
_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

# アプリを読み込む（main または app.main）
try:
    from main import app
except ModuleNotFoundError:
    try:
        from app.main import app
    except ModuleNotFoundError as e:
        raise ImportError(
            "FastAPI の app が見つかりません。backend 直下に main.py を置くか、"
            "conftest.py の import をあなたのアプリのモジュールに合わせて変更してください。"
        ) from e


@pytest.fixture
def client() -> TestClient:
    """FastAPI アプリに対する TestClient を返す。"""
    return TestClient(app)
