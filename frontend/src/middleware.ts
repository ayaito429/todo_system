import { NextRequest, NextResponse } from "next/server";

// 認証チェックを行うパスだけに限定（/login では実行しない）
export const config = {
  matcher: ["/tasks", "/tasks/:path*"],
};

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;

  if (!token) {
    const loginUrl = new URL("/", request.url);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}
