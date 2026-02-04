// API レスポンス型（TODO: エンドポイントに合わせて拡張）
export type ApiError = {
  detail: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};
