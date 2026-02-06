// fetch のベース（BASE_URL, ヘッダー）
// サーバー（Docker 内）→ API_SERVER_URL（backend:8000）
// ブラウザ or ローカルサーバー → NEXT_PUBLIC_API_URL（localhost:8000）
export const apiClient = {
  baseUrl:
    (typeof window === "undefined"
      ? process.env.API_SERVER_URL
      : undefined) ??
    process.env.NEXT_PUBLIC_API_URL ??
    "",
};
