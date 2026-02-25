"use client";
// AuthProvider, useAuth（JWT保持・ロール）（TODO: 実装）
export function AuthProvider({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}

export function useAuth() {
  return { user: null, isAuthenticated: false };
}
