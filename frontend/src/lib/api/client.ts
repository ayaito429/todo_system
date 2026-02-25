// fetch のベース（BASE_URL, ヘッダー）
// サーバー（Docker 内）→ API_SERVER_URL（backend:8000）
// ブラウザ or ローカルサーバー → NEXT_PUBLIC_API_URL（localhost:8000）
export const apiClient = {
  baseUrl:
    (typeof window === "undefined" ? process.env.API_SERVER_URL : undefined) ??
    process.env.NEXT_PUBLIC_API_URL ??
    "",
};

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

export function getAuthHeaders(): HeadersInit {
  const token = getAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}
