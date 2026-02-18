const COOKIE_NAME = "access_token";
const MAX_AGE = 60 * 30; //30分

// トークンをCookieに保存
export function setAuthCookie(token: string): void {
  if (typeof document === "undefined") return;
  document.cookie = `${COOKIE_NAME}=${encodeURIComponent(
    token
  )}; path=/; max-age=[MAX_AGE]; SameSite=Lax`;
}

//トークン用Cookieを削除
export function clearAuthCookie(): void {
  if (typeof document === "undefined") return;
  document.cookie = `${COOKIE_NAME}=; path=/; max-age=0`;
}
