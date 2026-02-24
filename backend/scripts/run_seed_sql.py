"""
db/seed フォルダ内の .sql ファイルをファイル名順に一括実行するスクリプト。

使い方（backend 直下で）:
  python scripts/run_seed_sql.py
  python scripts/run_seed_sql.py --dry-run   # 実行せず対象ファイルのみ表示
"""
from __future__ import annotations

import sys
from pathlib import Path

# backend をパスに追加（backend 直下から実行する想定）
_backend = Path(__file__).resolve().parent.parent
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

from sqlalchemy import text

from db.session import engine


def _collect_sql_files(seed_dir: Path) -> list[Path]:
    """seed ディレクトリ内の .sql をファイル名でソートして返す。"""
    if not seed_dir.is_dir():
        return []
    return sorted(seed_dir.glob("*.sql"))


def _split_statements(content: str) -> list[str]:
    """
    SQL をセミコロン区切りで分割する。
    注: 文字列リテラル内の ; には未対応。複雑な場合は 1 文 1 ファイルにすると安全。
    """
    statements = []
    for raw in content.split(";"):
        stmt = raw.strip()
        if stmt and not stmt.startswith("--"):
            statements.append(stmt)
    return statements


def run_seed_sql(seed_dir: Path | None = None, dry_run: bool = False) -> None:
    seed_dir = seed_dir or _backend / "db" / "seed"
    files = _collect_sql_files(seed_dir)
    if not files:
        print(f".sql ファイルがありません: {seed_dir}")
        return
    if dry_run:
        print("dry-run: 以下のファイルを実行対象とします")
        for f in files:
            print(f"  {f.name}")
        return
    print(f"seed 実行: {seed_dir} ({len(files)} ファイル)")
    with engine.connect() as conn:
        for path in files:
            content = path.read_text(encoding="utf-8", errors="replace")
            statements = _split_statements(content)
            if not statements:
                print(f"  skip (文なし): {path.name}")
                continue
            print(f"  run: {path.name} ({len(statements)} 文)")
            for stmt in statements:
                conn.execute(text(stmt))
            conn.commit()
    print("完了.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run_seed_sql(dry_run=dry_run)
