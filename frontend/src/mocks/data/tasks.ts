import { Task } from "@/src/types/task";

export const mockTasks: Task[] = [
  {
    id: 1,
    title: "フロント実装の骨組み作成",
    description: "Next.jsのApp Routerで一覧画面のレイアウトを作成する。サイドバーとヘッダーの共通コンポーネントを含む。",
    status: "未着手",
    priority: 1,
    user: { id: 101, name: "田中 太郎", role: "admin" },
    due_date: "2023-11-10",
    created_at: "2023-10-27T10:00:00Z",
    updated_at: "2023-10-27T10:00:00Z",
  },
  {
    id: 2,
    title: "API疎通テスト",
    description: "バックエンドのFastAPIと連携確認。CORS設定のチェックも行う。",
    status: "完了",
    priority: 2,
    user: { id: 102, name: "佐藤 次郎", role: "user" },
    due_date: "2023-11-15",
    created_at: "2023-10-28T09:00:00Z",
    updated_at: "2023-10-28T09:00:00Z",
  },
  {
    id: 3,
    title: "バグ修正：ログインエラー",
    description: "特定の条件下でセッションが切れる問題を調査・修正する。再現環境の構築から開始。",
    status: "対応中",
    priority: 1,
    user: { id: 101, name: "田中 太郎", role: "admin" },
    due_date: "2023-10-30", // 期限間近の設定
    created_at: "2023-10-29T14:00:00Z",
    updated_at: "2023-10-30T10:30:00Z",
  },
  {
    id: 4,
    title: "デザイン微調整",
    description: "UIのパディングとフォントサイズの微調整。モバイル表示での崩れを確認して修正する。",
    status: "未着手",
    priority: 3,
    user: { id: 103, name: "山田 花子", role: "user" },
    due_date: undefined, // 期限なしのパターン
    created_at: "2023-10-30T08:00:00Z",
    updated_at: "2023-10-30T08:00:00Z",
  },
  {
    id: 5,
    title: "非常に長いタイトルのテスト。このタイトルはどこまで表示されるか、レイアウトが崩れないかを確認するために長くしています。三点リーダーなどが適切に表示されることが望ましいです。",
    description: "詳細文も長くします。長い文章を入れることで、カードの高さがどう変化するか、またはスクロールが発生するかを確認します。",
    status: "対応中",
    priority: 2,
    user: { id: 104, name: "鈴木 一郎", role: "user" },
    due_date: "2023-12-31",
    created_at: "2023-10-31T12:00:00Z",
    updated_at: "2023-10-31T12:00:00Z",
  }
];
