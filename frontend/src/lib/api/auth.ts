import { apiClient } from "./client";

type LoginResponse = {
  access_token: string;
  token_type: string;
};

// POST /auth/login（TODO: 実装）
export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const url = `${apiClient.baseUrl}/auth/login`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.message ?? "ログインに失敗しました");
  }
  return res.json() as Promise<LoginResponse>;
}
