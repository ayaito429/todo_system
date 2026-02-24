import { Task, TaskCreate, TaskInitResponse } from "@/src/types/task";
import { apiClient, getAuthHeaders } from "./client";

// タスク一覧取得
export async function getTeamTasks() {
  const url = `${apiClient.baseUrl}/api/team/tasks`;
  const res = await fetch(url, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) {
    throw new Error(`チームタスクが見つかりませんでした: ${res.status}`);
  }
  const data = await res.json();
  return data;
}
