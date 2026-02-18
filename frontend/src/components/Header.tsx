"use client";
import { LogIn } from "lucide-react";
import Link from "next/link";
import { logout } from "../lib/auth";

export function Header() {
  return (
    <header className="bg-white h-16 flex px-30">
      <div className="flex justify-between w-full items-center">
        <Link href="/tasks">
          <div className="flex items-center space-x-2">
            <svg
              width="40"
              height="40"
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
            <span className="font-bold">Task Flow</span>
          </div>
        </Link>
        <div className="flex space-x-5">
          <span>ユーザー名</span>
          <button onClick={() => logout()}>
            <LogIn />
          </button>
        </div>
      </div>
    </header>
  );
}
