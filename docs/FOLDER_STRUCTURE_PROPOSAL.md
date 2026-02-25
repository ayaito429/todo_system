# Enterprise Task Hub — フォルダ構成提案

設計書「業務管理アプリ Enterprise Task Hub 最終設計書」に基づく、**バックエンド（FastAPI）** と **フロントエンド（Next.js）** のディレクトリ構造案です。

---

## 1. バックエンド（FastAPI）

```
backend/
├── main.py                    # アプリ起動・ルーター登録
├── config.py                  # 環境変数・DB接続設定
├── requirements.txt
│
├── core/                      # 認証・認可の核
│   ├── __init__.py
│   ├── security.py            # JWT発行・検証、password_hash
│   ├── permissions.py         # 権限マトリクスロジック（Admin/Leader/User 判定）
│   └── dependencies.py        # get_current_user 等のFastAPI Depends
│
├── db/                        # DB接続・セッション
│   ├── __init__.py
│   ├── session.py             # SessionLocal, get_db
│   └── base.py                # Base, metadata（必要に応じて）
│
├── models/                    # SQLAlchemyモデル（ER図準拠）
│   ├── __init__.py
│   ├── team.py                # teams
│   ├── user.py                # users (role, team_id)
│   └── task.py                # tasks (created_by, user_id, deleted_flag)
│
├── schemas/                   # Pydantic（リクエスト/レスポンス）
│   ├── __init__.py
│   ├── auth.py                # LoginRequest, Token
│   ├── user.py                # UserResponse, UserCreate 等
│   ├── team.py                # TeamResponse 等
│   └── task.py                # TaskCreate, TaskUpdate, TaskResponse
│
├── repositories/              # DBアクセス層（オプション；サービスに統合可）
│   ├── __init__.py
│   ├── user_repository.py
│   ├── team_repository.py
│   └── task_repository.py
│
├── services/                  # ビジネスロジック・認可と組み合わせ
│   ├── __init__.py
│   ├── auth_service.py        # ログイン処理
│   ├── task_service.py        # 一覧WHERE句の動的変更、CRUD＋権限チェック
│   ├── team_service.py        # チームCRUD（管理者のみ編集等）
│   └── user_service.py
│
├── routers/                   # APIエンドポイント
│   ├── __init__.py
│   ├── auth.py                # POST /auth/login
│   ├── tasks.py               # GET/POST /tasks, GET/PATCH/DELETE /tasks/{id}
│   ├── teams.py               # チーム管理（必要に応じて）
│   └── users.py               # ユーザー一覧等（必要に応じて）
│
└── scripts/                   # サンプルデータ投入等
    ├── __init__.py
    └── seed_data.py           # 10万タスク・20ユーザー・3チーム生成
```

### 設計書との対応メモ

- **権限マトリクス**: `core/permissions.py` で「管理者/リーダー/一般」ごとの操作可否を実装し、`services/task_service.py` および `routers/tasks.py` から利用。
- **API一覧**: `routers/auth.py` と `routers/tasks.py` が設計書のパス・メソッド・認可ルールを担当。
- **ER図**: `models/team.py`, `user.py`, `task.py` で teams / users / tasks を定義。

---

## 2. フロントエンド（Next.js, App Router）

```
frontend/
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── postcss.config.mjs
├── public/
│
└── src/
    ├── app/
    │   ├── layout.tsx                 # ルートレイアウト
    │   ├── page.tsx                   # トップ（例: / から /tasks へリダイレクト等）
    │   ├── globals.css
    │   ├── favicon.ico
    │   │
    │   ├── login/
    │   │   └── page.tsx               # ログイン画面 (/login)
    │   │
    │   └── tasks/
    │       ├── layout.tsx             # 一覧ベースのレイアウト
    │       ├── page.tsx               # 一覧画面 (/tasks)
    │       ├── new/
    │       │   └── page.tsx           # 新規作成（モーダル用）(/tasks/new)
    │       ├── [id]/
    │       │   └── page.tsx           # 詳細・編集（モーダル用）(/tasks/[id])
    │       └── _components/           # タスク関連の局所コンポーネント（任意）
    │           └── TaskModal.tsx
    │
    ├── components/                    # 共通UI
    │   ├── ui/                        # shadcn/ui 等のプリミティブ（Day 12–14で導入想定）
    │   │   └── ...
    │   ├── PriorityDot.tsx
    │   ├── StatusBadge.tsx
    │   ├── TaskCard.tsx
    │   └── TaskForm.tsx               # 新規/編集フォーム（共有化）
    │
    ├── lib/                           # API・認証・ユーティリティ
    │   ├── api/
    │   │   ├── client.ts              # fetch のベース（BASE_URL, ヘッダー）
    │   │   ├── auth.ts                # POST /auth/login
    │   │   └── tasks.ts               # GET/POST/PATCH/DELETE /tasks
    │   ├── auth/
    │   │   ├── context.tsx            # AuthProvider, useAuth（JWT保持・ロール）
    │   │   └── guard.tsx              # 認可に応じたUIの出し分け・ガード
    │   └── constants.ts              # ロール名、ステータス、優先度ラベル等
    │
    ├── types/                         # 型定義
    │   ├── task.ts
    │   ├── user.ts                    # User, Role
    │   └── api.ts                     # APIレスポンス型
    │
    └── mocks/                         # 開発用モック（必要なら残す）
        └── data/
            └── tasks.ts
```

### 設計書との対応メモ

- **画面一覧・URL**:  
  - `/login` → `app/login/page.tsx`  
  - `/tasks` → `app/tasks/page.tsx`  
  - `/tasks/new` → `app/tasks/new/page.tsx`（新規モーダル）  
  - `/tasks/[id]` → `app/tasks/[id]/page.tsx`（詳細・編集モーダル）
- **パラレルルート / インターセプティングルート**:  
  モーダルを「URL直叩きでも開く」ようにする場合は、例えば `app/tasks/@modal/(.)new/page.tsx` と `app/tasks/@modal/(.)tasks/[id]/page.tsx` のような **Parallel Routes** と **Intercepting Routes** を追加する構成にすると、一覧をベースにしたままURLと連動できます。上記は「まずはシンプルに `new` と `[id]` でページ」とした案です。必要なら `@modal` 用のサブフォルダを追加してください。
- **権限とUI**: `lib/auth/guard.tsx` で「管理者はチーム編集」「一般は自分のタスクのみ編集」などの出し分けを実装。

---

## 3. ルート直下（リポジトリ全体）

```
todo_system/   （または enterprise-task-hub/）
├── docker-compose.yml         # app, db (PostgreSQL)
├── Dockerfile                 # バックエンド or マルチステージで frontend も
├── README.md
├── .gitignore
├── backend/                   # 上記 1 の構成
├── frontend/                  # 上記 2 の構成
└── docs/
    └── FOLDER_STRUCTURE_PROPOSAL.md   # 本ドキュメント
```

---

## 4. 補足

- **バックエンド**: `repositories` を廃止し、`services` 内で直接 SQLAlchemy を触る構成も可能です。チームの好みで「repository 層あり/なし」を選べます。
- **フロントエンド**: 状態管理はまず React Context（`lib/auth/context.tsx`）で足り、タスク一覧は Server Components と `fetch` で十分です。必要になったら TanStack Query 等を追加する想定です。
- **認可**: バックエンドで「必ず `core/permissions.py` 経由で判定する」と決めておくと、設計書の権限マトリクスを一箇所で守りやすくなります。

以上が、設計書に基づくフォルダ構成の提案です。
