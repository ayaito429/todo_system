import { Task , TaskCreate } from "@/src/types/task";
import { apiClient } from "./client";

// GET/POST/PATCH/DELETE /tasks（TODO: 実装）
export async function getTasks():Promise<Task[]> {
  const url = `${apiClient.baseUrl}/tasks`;
  const res = await fetch(url);
  if(!res.ok) {
    throw new Error(`タスクが見つかりませんでした: ${res.status}`)
    }
    const data = await res.json();
  return data as Task[];
}

export async function createTask(body:Promise<TaskCreate>) {
  const url = `${apiClient.baseUrl}/tasks`;
  const res = await fetch(url, {
    method: "POST",
    body: JSON.stringify(body),
  });
  if(!res.ok) {
    throw new Error(`タスク作成に失敗しました: ${res.status}`)
  }
  const data = await res.json();
  return data as Task
}