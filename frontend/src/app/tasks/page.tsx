'use client';
import {useState} from "react";
import NewTaskModal from "@/src/components/NewTaskModal";
import TaskCard from "@/src/components/TaskCard";
import { getTasks } from "@/src/lib/api/tasks";
import { mockTasks } from "@/src/mocks/data/tasks";
import Link from "next/link";
import { Task } from "@/src/types/task";

export default function TaskListPage() {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  // const tasks = await getTasks();
const tasks = mockTasks
  return (
    <div>
      <h1>タスク一覧</h1>
      <Link href={"/tasks/new"}>新規作成</Link>
      <div>
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} onClick={() => setSelectedTask(task)}/>
        ))}
      </div>
      {selectedTask && (
        <NewTaskModal task={selectedTask} onClose={() => setSelectedTask(null)}/>
      )}
    </div>
  );
}
