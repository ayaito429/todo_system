export type TaskStatus = "未着手" | "対応中" | "完了";
export type TaskPriority = "高" | "中" | "低"; //1:高 2:中 3:低

//タスク一覧の型
export type Task = {
  id: number;
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  due_date?: string;
  user: {
    id: number;
    name: string;
    role: string;
  };
  created_at: string;
  created_by: string;
  updated_at: string;
  deleted_at?: string;
};

//タスク作成の型
export type TaskCreate = {
  title: string;
  description?: string;
  status: TaskStatus;
  priority: TaskPriority;
  user_id?: number;
  due_date?: string;
  created_by?: number;
  updated_by?: number;
  deleted_by?: number;
  deleted_at?: string;
  deleted_flag?: boolean;
  login_user: number;
}
