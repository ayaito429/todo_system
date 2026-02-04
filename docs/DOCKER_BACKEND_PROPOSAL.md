# バックエンド Docker 接続のベストプラクティス提案

## 方針

- **Dockerfile**: `backend/` 配下に置き、バックエンド単体でビルド可能にする（コンテキストは `backend/`）。
- **docker-compose**: `backend` サービスを追加し、`db` の起動完了を待ってから FastAPI を起動する。
- **接続**: 環境変数で `DATABASE_URL`（または `POSTGRES_*`）を渡し、コンテナ間はサービス名 `db` で名前解決。

---

## 1. 推奨ディレクトリ構成

```
todo_system/
├── docker-compose.yml      # db + backend を定義
├── backend/
│   ├── Dockerfile          # バックエンド用
│   ├── requirements.txt    # バックエンド専用（DB接続ライブラリ含む）
│   └── main.py
└── ...
```

- ルートの `requirements.txt` はローカル開発用、`backend/requirements.txt` は Docker ビルド用として分けてもよいです（本提案では `backend/requirements.txt` を Docker で使う形にしています）。

---

## 2. 接続の流れ

1. `docker compose up` で `db` と `backend` が起動。
2. `backend` は `depends_on`（＋オプションで `condition: service_healthy`）で **PostgreSQL の準備ができてから** 起動。
3. バックエンドは環境変数 `DATABASE_URL=postgresql://...@db:5432/...` で `db` コンテナに接続（`db` はサービス名で名前解決される）。
4. フロントエンドや外部からは `backend` のポート（例: 8000）にアクセス。

---

## 3. ベストプラクティス要点

| 項目 | 推奨 |
|------|------|
| **DB 待機** | `depends_on` に `condition: service_healthy` を付け、`db` の healthcheck が通ってから `backend` を起動する。 |
| **接続文字列** | 本番は `DATABASE_URL` 1本で渡す。開発用は `POSTGRES_USER` 等を compose で渡し、アプリで `DATABASE_URL` を組み立てても可。 |
| **シークレット** | 本番では `env_file` や Docker Secrets / クラウドの環境変数を使い、パスワードを compose に直書きしない。 |
| **開発時のホットリロード** | `backend` に `volumes: [.:/app]` をマウントし、`uvicorn --reload` で起動する。 |
| **ネットワーク** | 明示しなくても default ネットワークで `backend` → `db` は通信可能。必要なら `networks:` で分離。 |

---

## 4. 作成・更新するファイル

- **backend/Dockerfile** … 新規
- **backend/requirements.txt** … 新規（Docker 用；SQLAlchemy・psycopg2 等を含む）
- **docker-compose.yml** … `backend` サービスと `db` の healthcheck を追加

以上の内容で、実際の `Dockerfile` と `docker-compose.yml` の案をリポジトリに追加しています。
