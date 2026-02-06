import { Task } from "../types/task";
import PriorityDot from "./PriorityDot";
import StatusBadge from "./StatusBadge";

type Props = {
  task: Task;
  onClick: () => void;
};

export default function TaskCard({ task ,onClick}: Props) {
  return (
    <div className="border-2 border-[#333] rounded-lg p-4 bg-white transition-all hover:bg-[#fafafa] hover:tranlate-x-[20px]" onClick={onClick}>
      <div className="flex items-center mb-2.5">
        <PriorityDot priority={task.priority} />
        <div>
          <button>詳細</button>
          <button>編集</button>
          <button>削除</button>
        </div>
      </div>
      <div>
        <StatusBadge status={task.status} />
        <span>公開</span>
        <span>{task.due_date || "期限なし"}</span>
        <span>{task.user.name || "未設定"}</span>
        <span>更新: {task.updated_at}</span>
      </div>
    </div>
  );
}
