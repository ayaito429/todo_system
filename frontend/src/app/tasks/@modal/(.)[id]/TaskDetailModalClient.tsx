import NewTaskModal from "@/src/components/NewTaskModal";
import { Task } from "@/src/types/task";
import { useRouter } from "next/navigation";

type Props = {
  task: Task;
};

export default function TaskDetailModalClient({ task }: Props) {
  const router = useRouter();

  if (!task) {
    return (
      <div className="bg-white p-6 rounded shadow-lg max-w-lg">
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
