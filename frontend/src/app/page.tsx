"use client";
import { changePasswordFirstTime, getMe, login } from "@/src/lib/api/auth";
import { setAuthCookie } from "@/src/lib/cookie";
import { Dice1, Eye, EyeOff } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useUser } from "../contexts/UserContext";

export default function Home() {
  const [showPassword, setShowPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [requirePasswordChange, setRequirePasswordChange] = useState(false);
  const [newPassword, setNewPassword] = useState("");
  const router = useRouter();
  const { setUser } = useUser();

  const handleSubmit = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await login(email, password);
      localStorage.setItem("access_token", data.access_token);
      setAuthCookie(data.access_token);

      if (data.require_password_change) {
        setRequirePasswordChange(true);
        return;
      }

      const user = await getMe(data.access_token);
      setUser(user);
      router.push("/tasks");
    } catch (err) {
      setError(err instanceof Error ? err.message : "ログインに失敗しました");
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChangeSubmit = async (
    e: React.FormEvent<HTMLFormElement>,
  ) => {
    e.preventDefault();

    const token = localStorage.getItem("access_token");
    if (!token) {
      return;
    }
    try {
      await changePasswordFirstTime(token, newPassword);
      const user = await getMe(token);
      setUser(user);
      router.push("/tasks");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "パスワードの変更に失敗しました",
      );
    }
  };
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-sm space-y-6">
        <div className="flex flex-col items-center">
          <svg
            width="60"
            height="60"
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="50" cy="50" r="48" stroke="#1F2937" strokeWidth="4" />
            <path
              d="M30 35H70M50 35V75M40 65L48 73L75 45"
              stroke="#3B82F6"
              strokeWidth="8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>

          <h1 className="text-2xl font-bold mt-5">Task Flow</h1>
          {error && <p className="text-red-600 text-sm">{error}</p>}
        </div>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (requirePasswordChange) {
              handlePasswordChangeSubmit(e as React.FormEvent<HTMLFormElement>);
            } else {
              handleSubmit(e);
            }
          }}
          className="space-y-4"
        >
          <div className="">
            <div className="flex flex-col space-y-2">
              <label htmlFor="">メールアドレス</label>
              <input
                type="email"
                className="border border-gray-200 rounded-md h-10"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="flex flex-col space-y-2">
              <label htmlFor="">パスワード</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  className="border border-gray-200 rounded-md h-10 w-full"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2"
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {requirePasswordChange && (
            <div className="flex flex-col space-y-2">
              <label htmlFor="new-password">新しいパスワード</label>
              <div className="relative">
                <input
                  id="new-password"
                  type={showNewPassword ? "text" : "password"}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="border border-gray-200 rounded-md h-10 w-full"
                  required={requirePasswordChange}
                />
                <button
                  type="button"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2"
                >
                  {showNewPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>
          )}

          <button
            type="submit"
            className="bg-blue-500 w-full text-white border rounded-lg h-10"
          >
            {requirePasswordChange
              ? "パスワードを更新"
              : loading
                ? "ログイン中..."
                : "ログイン"}
          </button>
        </form>
      </div>
    </div>
  );
}
