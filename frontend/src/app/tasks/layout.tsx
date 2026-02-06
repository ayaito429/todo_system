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
  {!isNewOpen && children}
  {isNewOpen && (
    <div onClick={() => router.push("/tasks")}>
      <div onClick={(e) => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )}
  </>

  )
}
