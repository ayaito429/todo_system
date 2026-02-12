"use client";

import { useEffect } from "react";
import TaskCard from "@/src/components/TaskCard";
import { getTasks } from "@/src/lib/api/tasks";
import Link from "next/link";
import { useTaskList } from "@/src/contexts/TaskListContent";

export default function TaskListPage() {
  const { tasks, setTasks } = useTaskList();
  const gridLayout =
    "grid grid-cols-[1fr_120px_100px_120px_120px] gap-4 item-center";

  useEffect(() => {
    getTasks()
      .then((data) => {
        console.log("一覧でーた", data);
        setTasks(data);
      })
      .catch(console.error);
  }, [setTasks]);

  console.log("tasks一覧", tasks);
  return (
    <div className="min-h-screen p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold tracking-tight">タスク一覧</h1>
        <Link href={"/tasks/new"}>新規作成</Link>
      </header>
      <div className="border rounded-lg">
        <div className={`${gridLayout} px-4 py-3 text-sm font-medium border-b`}>
          <div>タスク名</div>
          <div>ステータス</div>
          <div>優先度</div>
          <div>期限</div>
          <div>担当者</div>
        </div>
        <div className="">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} layout={gridLayout} />
          ))}
        </div>
      </div>
    </div>
  );
}
