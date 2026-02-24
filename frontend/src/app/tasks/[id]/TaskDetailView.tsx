"use client";
import NewTaskModal from "@/src/components/NewTaskModal";
import { useTaskList } from "@/src/contexts/TaskListContent";
import { getTasks } from "@/src/lib/api/tasks";
import { Task } from "@/src/types/task";
import { notFound, useParams, useRouter } from "next/navigation";
import { useState, useMemo, useEffect } from "react";

export default function TaskDetailView() {
  const params = useParams();
  const router = useRouter();
  const { tasks } = useTaskList();

  const id = Number(params.id);
  const [fallbackTasks, setFallbackTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  const taskFromContext = useMemo(
    () => tasks.find((t) => t.id === id),
    [tasks, id],
  );

  useEffect(() => {
    if (taskFromContext || tasks.length > 0) return;
    setLoading(true);
    getTasks()
      .then((all) => setFallbackTasks(all.tasks))
      .finally(() => setLoading(false));
  }, [taskFromContext, tasks.length]);

  const task = taskFromContext ?? fallbackTasks.find((t) => t.id === id);

  if (loading) return <p>読み込み中...</p>;

  if (!task) {
    return (
      <div>
        <p>タスクが見つかりません</p>
        <button
          type="button"
          onClick={() => router.push("/tasks")}
          className="mt-2 text-blue-600 underline"
        >
          一覧に戻る
        </button>
      </div>
    );
  }

  return (
    <div>
      <NewTaskModal
        task={task}
        mode="view"
        onClose={() => router.push("/tasks")}
      />
    </div>
  );
}
