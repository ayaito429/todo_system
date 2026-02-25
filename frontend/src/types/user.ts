// User, Role（TODO: API レスポンスに合わせて拡張）
export type Role = "admin" | "leader" | "user";

export type User = {
  id?: number;
  name: string;
  email: string;
  role: Role;
  team_id: number | null;
  password: string;
};
