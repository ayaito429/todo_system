import { Task } from "@/src/types/task";

export const mockTasks: Task[] = [
  {
    id: 1,
    title: "フロント実装の骨組み作成",
    description: "Next.jsのApp Routerで一覧画面のレイアウトを作成する",
    status: "doing",
    priority: 1,
    user: {
      id: 101,
      name: "田中 太郎",
      role: "admin",
    },
    due_date: "2023-11-10",
    created_at: "2023-10-27T10:00:00Z",
    updated_at: "2023-10-27T10:00:00Z",
  },
  {
    id: 2,
    title: "API疎通テスト",
    description: "バックエンドのFastAPIと連携確認",
    status: "todo",
    priority: 2,
    user: {
      id: 102,
      name: "佐藤 次郎",
      role: "user",
    },
    due_date: "2023-11-15",
    created_at: "2023-10-28T09:00:00Z",
    updated_at: "2023-10-28T09:00:00Z",
  },
];
