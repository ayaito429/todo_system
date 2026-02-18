import { clearAuthCookie } from "./cookie";

export function logout(): void {
  localStorage.removeItem("access_token");
  clearAuthCookie();
  window.location.href = "/";
}
