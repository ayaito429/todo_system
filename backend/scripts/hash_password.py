"""
SQL の INSERT 用にパスワードを Argon2 ハッシュ化して表示する。
使い方（backend ディレクトリで）:
  python scripts/hash_password.py
  python scripts/hash_password.py mypassword
"""
import sys
from pathlib import Path

# backend をパスに追加（backend 直下から実行する想定）
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from core.security import get_password_hash


def main():
    password = sys.argv[1] if len(sys.argv) > 1 else "password"
    hashed = get_password_hash(password)
    print(hashed)


if __name__ == "__main__":
    main()
