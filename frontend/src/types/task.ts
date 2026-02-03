export type TaskStatus = "todo" | "doing" | "done";
export type TaskPriority = 1 | 2 | 3; //1:高 2:中 3:低

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
  updated_at: string;
  deleted_at?: string;
};
