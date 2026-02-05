# バックエンド実装手順

DB から順に進めるのがおすすめです。依存関係が下から上になるため、迷いにくくテストもしやすいです。

---

## 1. DB の起動と接続（最初にやること）

1. **PostgreSQL を起動する**
   ```bash
   docker compose up -d db
   ```
   - `docker-compose.yml` で `todo_system_dev` DB・ユーザーが定義済みです。

2. **接続確認**
   ```bash
   docker compose exec db psql -U todo_user -d todo_system_dev -c "\dt"
   ```
   - 最初はテーブルなしで OK です。

---

## 2. 設定・DB 接続層（config / session）

| 順 | ファイル | 内容 |
|----|----------|------|
| 1 | `backend/config.py` | 環境変数（`DATABASE_URL` 等）を `pydantic-settings` で読み込み |
| 2 | `backend/db/base.py` | SQLAlchemy の `Base`, `metadata` |
| 3 | `backend/db/session.py` | エンジン・`SessionLocal`・`get_db()` |

このあと「モデル定義 → マイグレーション or create_all」の流れになります。

---

## 3. モデル（ORM）

| 順 | ファイル | 内容 |
|----|----------|------|
| 1 | `backend/models/user.py` | ユーザーテーブル（id, email, hashed_password 等） |
| 2 | `backend/models/task.py` | タスクテーブル（user_id などで User と関連） |
| 3 | `backend/models/__init__.py` | 全モデルを import し、`Base.metadata` を一箇所でまとめる（マイグレーション用） |

---

## 4. テーブル作成

- **開発初期**: `Base.metadata.create_all(bind=engine)` を起動時に実行する方法が簡単です。
- **運用を見据える場合**: Alembic を導入し、マイグレーションでテーブル作成・変更する方法がおすすめです。

---

## 5. 認証まわり（JWT）

| 順 | ファイル | 内容 |
|----|----------|------|
| 1 | `backend/core/security.py` | パスワードハッシュ（bcrypt）、JWT 生成・検証 |
| 2 | `backend/schemas/auth.py` | `LoginRequest`, `Token` 等の Pydantic スキーマ |
| 3 | `backend/core/dependencies.py` | `get_current_user`（Bearer トークンから User 取得） |
| 4 | `backend/repositories/user_repository.py` | `get_user_by_email` 等 |
| 5 | `backend/services/auth_service.py` | ログイン処理（パスワード照合 → トークン発行） |
| 6 | `backend/routers/auth.py` | `POST /auth/login` |

---

## 6. タスク API

| 順 | ファイル | 内容 |
|----|----------|------|
| 1 | `backend/schemas/task.py` | タスクの Request/Response スキーマ |
| 2 | `backend/repositories/task_repository.py` | CRUD |
| 3 | `backend/services/task_service.py` | ビジネスロジック（必要なら） |
| 4 | `backend/routers/tasks.py` | `GET/POST /tasks`, `GET/PUT/DELETE /tasks/{id}` |
| 5 | `backend/main.py` | `app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])` 等でルーター登録 |

---

## 7. その他

- **ユーザー API**（`/users`）: 認証後に「自分」の情報取得・更新など。
- **チーム**（`teams`）: 必要ならモデル・リポジトリ・ルーターを同様の順で追加。
- **CORS**: フロント（Next.js）から呼ぶ場合は `main.py` で CORS を有効化。

---

## 進め方のコツ

1. **DB → config → session → モデル → テーブル作成** までを一気にやって、`docker compose up` でアプリ起動・テーブル作成できる状態にする。
2. **認証（ログイン）** を実装して、`POST /auth/login` でトークンが返ることを確認する。
3. **タスク CRUD** を実装し、`Authorization: Bearer <token>` で動作確認する。

不明点や「このファイルから具体的に書きたい」があれば、そのファイル名を指定してもらえればコード例まで書きます。
