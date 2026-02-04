// User, Role（TODO: API レスポンスに合わせて拡張）
export type Role = "ADMIN" | "LEADER" | "USER";

export type User = {
  id: number;
  name: string;
  email: string;
  role: Role;
  team_id: number | null;
};
