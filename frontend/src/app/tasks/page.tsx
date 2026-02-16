"use client";

import { useEffect, useState } from "react";
import TaskCard from "@/src/components/TaskCard";
import { getTasks } from "@/src/lib/api/tasks";
import Link from "next/link";
import { useTaskList } from "@/src/contexts/TaskListContent";

const PAGE_SIZE = 8;

export default function TaskListPage() {
  const { tasks, setTasks } = useTaskList();
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(tasks.length / PAGE_SIZE) || 1;
  const start = (currentPage - 1) * PAGE_SIZE;
  const displayedTasks = tasks.slice(start, start + PAGE_SIZE);

  const gridLayout =
    "grid grid-cols-[1fr_120px_100px_120px_120px] gap-4 items-center";

  useEffect(() => {
    getTasks()
      .then((data) => {
        setTasks(data);
      })
      .catch(console.error);
  }, [setTasks]);

  return (
    <div className="min-h-screen p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold tracking-tight">タスク一覧</h1>
        <Link href={"/tasks/new"} className="border rounded p-2 bg-green-200">
          新規作成
        </Link>
      </header>
      <div className="border rounded-lg">
        <div className={`${gridLayout} px-4 py-3 text-sm font-medium border-b`}>
          <div>タスク名</div>
          <div>ステータス</div>
          <div>優先度</div>
          <div>期限</div>
          <div>担当者</div>
        </div>
        <div className="bg-white">
          {displayedTasks.map((task) => (
            <TaskCard key={task.id} task={task} layout={gridLayout} />
          ))}
        </div>
      </div>
      {totalPages > 1 && (
        <div className="flex items-center">
          <button
            type="button"
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p - 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            前へ
          </button>
          <span className="px-2">
            {currentPage}/{totalPages}
          </span>
          <button
            type="button"
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            次へ
          </button>
        </div>
      )}
    </div>
  );
}
