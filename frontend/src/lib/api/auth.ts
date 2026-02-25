import { apiClient } from "./client";

type LoginResponse = {
  access_token: string;
  token_type: string;
  require_password_change: boolean;
};

type MeResponse = {
  user_id: number;
  email: string;
  role: string;
  name: string;
};

// POST /auth/login（TODO: 実装）
export async function login(
  email: string,
  password: string,
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

export async function getMe(token: string) {
  const url = `${apiClient.baseUrl}/auth/me`;
  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!res.ok) throw new Error("ユーザー情報の取得に失敗しました");
  console.log("res",res)
  return res.json() as Promise<MeResponse>;
}

export async function changePasswordFirstTime(
  token: string,
  newPassword: string,
): Promise<void> {
  const url = `${apiClient.baseUrl}/auth/first-login/password`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ new_password: newPassword }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.message ?? "パスワードの変更に失敗しました");
  }
}
