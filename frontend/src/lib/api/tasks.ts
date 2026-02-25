import { Task, TaskCreate, TaskInitResponse } from "@/src/types/task";
import { apiClient, getAuthHeaders } from "./client";

// タスク一覧取得
export async function getTasks(): Promise<TaskInitResponse> {
  const url = `${apiClient.baseUrl}/api/tasks`;
  const res = await fetch(url, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    throw new Error(`タスクが見つかりませんでした: ${res.status}`);
  }
  const data = await res.json();
  return data as TaskInitResponse;
}

// タスク作成
export async function createTask(body: TaskCreate) {
  const url = `${apiClient.baseUrl}/api/tasks`;
  const res = await fetch(url, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`タスク作成に失敗しました: ${res.status}`);
  }
  const data = await res.json();
  return data as Task;
}

// //タスク更新
export async function updateTask(id: number, body: TaskCreate) {
  const url = `${apiClient.baseUrl}/api/tasks/${id}`;
  const res = await fetch(url, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`タスクが更新できませんでした: ${res.status}`);
  }
  return (await res.json()) as Task;
}

//タスクの削除
export async function deleteTask(id: number) {
  const url = `${apiClient.baseUrl}/api/tasks/${id}`;
  const res = await fetch(url, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    throw new Error(`タスクが削除できませんでした: ${res.status}`);
  }
  return await res;
}
