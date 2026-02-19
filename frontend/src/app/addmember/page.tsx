"use client";
import { useState } from "react";
import { Header } from "@/src/components/Header";
import { Eye, EyeOff } from "lucide-react";
import { useRouter } from "next/navigation";
import { createUser } from "@/src/lib/api/user";
import { Role } from "@/src/types/user";

export default function AddMember() {
  const [userName, setUserName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [role, setRole] = useState<Role>("user");
  const [teamId, setTeamId] = useState("");
  const router = useRouter();

  const handleCreate = async () => {
    try {
      await createUser({
        name: userName,
        email: email,
        role: role,
        password: password,
        team_id: Number(teamId),
      });
      router.push("/tasks");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Header />
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
            {/* {error && <p className="text-red-600 text-sm">{error}</p>} */}
            <h1 className="text-2xl p-5">メンバー登録</h1>
          </div>
          <form className="space-y-4">
            <div className="">
              <div className="flex flex-col space-y-2">
                <label htmlFor="">ユーザー名</label>
                <input
                  type="text"
                  className="border border-gray-200 rounded-md h-10"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                />
              </div>
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
              <div className="flex flex-col">
                <label htmlFor="">ロール</label>
                <select
                  name=""
                  id=""
                  value={role}
                  onChange={(e) => setRole(e.target.value as Role)}
                  className="border border-gray-200 rounded-md h-10 w-full"
                >
                  <option value="user">ユーザー</option>
                  <option value="leader">リーダー</option>
                  <option value="admin">管理者</option>
                </select>
              </div>
              <div className="flex flex-col">
                <label htmlFor="">チームID</label>
                <input
                  type="number"
                  name=""
                  id=""
                  value={teamId}
                  min={1}
                  onChange={(e) => setTeamId(e.target.value)}
                  className="border border-gray-200 rounded-md h-10"
                />
              </div>
            </div>

            <button
              type="button"
              className="bg-blue-500 w-full text-white border rounded-lg h-10"
              onClick={handleCreate}
            >
              登録
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
