# フロントエンド実装の手順

CRUD 先行のスケジュールに合わせた、**やる順番**です。上から順に進めると、認証なしでタスク操作 → そのあと認証を足す流れになります。

---

## 前提

- バックエンドの **GET /tasks**, **POST /tasks**, **GET/PATCH/DELETE /tasks/{id}** が動いていること（認証なしで OK）。
- フロントは `npm run dev` で起動し、`http://localhost:3000` で開けること。

---

## Phase 1：認証なしでタスク CRUD を動かす（Day 3〜7）

### Step 1. 環境変数と API の向き先

1. **`frontend/.env.local`** を作成する（Git にコミットしない）。
2. 次を書く（バックエンドの URL に合わせる）:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
3. `lib/api/client.ts` で `baseUrl` をこの値から読むようにする（すでに `process.env.NEXT_PUBLIC_API_URL` を参照していればそのままでよい）。
4. バックエンドで CORS が `http://localhost:3000` を許可しているか確認する。

**確認**: ブラウザの開発者ツールで、フロントから `http://localhost:8000` にリクエストが飛ぶこと。

---

### Step 2. 型定義を API に合わせる

1. **`types/task.ts`** を、バックエンドのレスポンスに合わせる。
   - 例: `status` が API で `"TODO" | "DOING" | "DONE"` なら、フロントも同じにする。
   - `id`, `title`, `description`, `status`, `priority`, `due_date`, `created_at`, `user`（担当者）など。
2. **新規作成用**の型を用意する（例: `TaskCreate`）。  
   `title`, `description?`, `status`, `priority`, `user_id?` など、POST で送るフィールドだけ。
3. **更新用**の型を用意する（例: `TaskUpdate`）。  
   PATCH で送るフィールドだけ（部分更新用に全部 optional でも可）。

**確認**: 型と API の JSON が一致していると、あとでハマりにくい。

---

### Step 3. API クライアント（tasks）を実装する

1. **`lib/api/client.ts`**
   - `baseUrl` は `process.env.NEXT_PUBLIC_API_URL ?? ""`。
   - `fetch` のラッパーを用意する（例: `get(url)`, `post(url, body)`, `patch(url, body)`, `delete(url)`）。  
     **Phase 1 では Authorization ヘッダーは不要。**
2. **`lib/api/tasks.ts`**
   - `getTasks()`: `GET /tasks` を呼び、`Task[]` を返す。
   - `getTask(id)`: `GET /tasks/{id}` を呼び、`Task` を返す。
   - `createTask(data: TaskCreate)`: `POST /tasks` で body を送り、作成された `Task` を返す。
   - `updateTask(id, data: TaskUpdate)`: `PATCH /tasks/{id}` で body を送る。
   - `deleteTask(id)`: `DELETE /tasks/{id}` を呼ぶ。
3. エラー時（`!res.ok`）は `throw new Error` やカスタムエラーにし、呼び出し側で catch できるようにする。

**確認**: Postman やブラウザではなく、フロントのコードから `getTasks()` を呼んで一覧が返ってくること。

---

### Step 4. タスク一覧ページ（/tasks）を API から表示する

1. **`app/tasks/page.tsx`**
   - `mockTasks` をやめ、**サーバーコンポーネント**なら `getTasks()` を呼んで `tasks` を取得し、`TaskCard` に渡す。
   - または **クライアントコンポーネント**（`"use client"`）にして、`useEffect` で `getTasks()` を呼び、`useState` で `tasks` を保持して表示する。
2. **ローディング・エラー**
   - 取得中は「読み込み中」、失敗時は「エラーです」などの表示を入れる。
3. **`TaskCard`**
   - 「詳細」ボタンを `Link` で `/tasks/[id]` に飛ばす（例: `<Link href={`/tasks/${task.id}`}>詳細</Link>`）。

**確認**: `/tasks` を開くと、バックエンドから取得したタスク一覧が表示される。

---

### Step 5. タスク詳細・編集・削除（/tasks/[id]）

1. **`app/tasks/[id]/page.tsx`**
   - パラメータで `id` を取得。`getTask(id)` で 1 件取得。
   - 表示用にタイトル・説明・ステータス・優先度・担当者・期限などを表示。
2. **編集**
   - フォーム（入力欄＋選択肢）で `title`, `description`, `status`, `priority` などを編集可能にする。
   - 送信時に `updateTask(id, { ... })` を呼ぶ。成功したら「更新しました」や一覧へ戻る。
3. **削除**
   - 「削除」ボタンを置き、クリックで確認ダイアログ → `deleteTask(id)` を呼ぶ。成功したら一覧（`/tasks`）へリダイレクト。
4. **ローディング・エラー・404**
   - 取得中・失敗時・存在しない id のときの表示を用意する。

**確認**: 一覧から詳細へ行き、編集・削除ができること。

---

### Step 6. 新規作成（/tasks/new）

1. **`app/tasks/new/page.tsx`**
   - フォーム: `title`（必須）, `description`, `status`, `priority`, `due_date` など。
   - 送信時に `createTask({ title, description, status, priority, ... })` を呼ぶ。
2. 成功したら「作成しました」のあと `/tasks` または `/tasks/{新規 id}` へ遷移する。
3. 一覧ページに「新規作成」リンクを置き、`/tasks/new` へ飛ばす。

**確認**: 新規作成 → 一覧に反映されること。

---

### Step 7. 一覧・詳細・新規のつながりと UI 調整（Day 6〜7）

1. 一覧の「詳細」→ 詳細ページ。「編集」は詳細ページの編集フォームでよい（または詳細ページに「編集」リンク）。
2. ヘッダーやナビに「タスク一覧」「新規作成」を置くとわかりやすい。
3. **マイルストーン**: 認証なしで、一覧・新規・詳細・編集・削除がすべてフロントからできる状態にする。

---

## Phase 2：認証を足す（Day 8〜）

### Step 8. ログイン API とトークン保存

1. **`lib/api/auth.ts`**
   - `login(email: string, password: string)` を実装。`POST /auth/login` を呼び、レスポンスの `access_token` と `user`（id, name, role, team_id 等）を返す。
2. **ログイン画面（`app/login/page.tsx`）**
   - メール・パスワードのフォーム。「ログイン」押下で `login()` を呼ぶ。
   - 成功したらトークンと user を **localStorage**（または Cookie）に保存し、`/tasks` へ `redirect()` する。
3. **AuthContext（`lib/auth/context.tsx`）**
   - 起動時に localStorage からトークン・user を読む。`user` と `setUser`、`token` と `setToken`、`isAuthenticated` を提供する。
   - ログイン成功時に `setToken` / `setUser` を呼ぶ。

**確認**: ログインすると `/tasks` に飛び、トークンが保存されていること。

---

### Step 9. 全 API に Authorization を付与する

1. **`lib/api/client.ts`**
   - 各 `fetch` のヘッダーに `Authorization: Bearer ${token}` を付ける。  
     token は引数で渡すか、localStorage から読む（または AuthContext から取得）。
2. **`lib/api/tasks.ts`**
   - `getTasks`, `getTask`, `createTask`, `updateTask`, `deleteTask` を、この client 経由で呼ぶようにする（すでに client を使っていれば、client 側で token を付けるだけでよい）。

**確認**: トークンなしで API を呼ぶと 401 になること。トークンありで成功すること。

---

### Step 10. 未認証時はログインへリダイレクト

1. **認証ガード**
   - タスク一覧・詳細・新規など「認証必須」のページで、トークンがなければ `/login` へ `redirect()` する。
   - クライアントコンポーネントなら、`useEffect` で token をチェックし、なければ `router.push("/login")`。
   - または `lib/auth/guard.tsx` で「子要素を表示するか、未認証なら /login へ」というラッパーを用意し、レイアウトで使う。
2. **ログアウト**
   - ヘッダーなどに「ログアウト」を置く。クリックで localStorage の token・user を削除し、`/login` へ飛ばす。

**確認**: ログアウト後は `/tasks` に直で行っても `/login` に飛ぶこと。

---

### Step 11. ロール表示と権限に応じた UI（Day 10〜）

1. AuthContext の `user` に `role` が入っているので、ヘッダーに「Admin」「Leader」「User」などを表示する。
2. 他人のタスクで「一般ユーザー」のときは、編集を「ステータスのみ」に制限する（フォームの項目を減らす or ボタンを「ステータスのみ更新」にする）。
3. API が 403 を返したときに「権限がありません」と表示する。

---

## チェックリスト（Phase 1 完了時）

- [ ] `.env.local` に `NEXT_PUBLIC_API_URL` を設定した
- [ ] 型（Task, TaskCreate, TaskUpdate）を API に合わせた
- [ ] `lib/api/client.ts` で baseUrl と fetch のラッパーを実装した
- [ ] `lib/api/tasks.ts` で getTasks, getTask, createTask, updateTask, deleteTask を実装した
- [ ] `/tasks` で API から一覧を取得して表示している
- [ ] `/tasks/[id]` で詳細・編集・削除ができる
- [ ] `/tasks/new` で新規作成でき、一覧に反映される
- [ ] 一覧・詳細・新規のリンクがつながっている

Phase 1 が終わったら Phase 2（Step 8〜）に進むと、スケジュールどおり「認証を足す」流れになります。
