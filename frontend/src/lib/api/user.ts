import { User } from "@/src/types/user";
import { apiClient, getAuthHeaders } from "./client";

export async function createUser(body: User) {
  const url = `${apiClient.baseUrl}/api/users`;
  const res = await fetch(url, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`ユーザーの作成に失敗しました: ${res.status}`);
  }
  const data = await res.json();
  return data;
}
