"use client";
import { usePathname, useRouter } from "next/navigation";

export default function TasksLayout({
  children,
}: {
  children: React.ReactNode;
}) {
const pathname = usePathname();
const router = useRouter();
const isNewOpen = pathname === "/tasks/new"

  return ( <>
  {children}
  {isNewOpen && (
    <div onClick={() => router.push("/tasks")}>
      <div onClick={(e) => e.stopPropagation()}>
        <h2>新規作成</h2>
        <button onClick={() => router.push("/tasks")}>閉じる</button>
      </div>
    </div>
  )}
  </>

  )
}
