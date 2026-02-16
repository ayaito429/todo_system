import Link from "next/link";
import { Task } from "../types/task";
import PriorityDot from "./PriorityDot";
import StatusBadge from "./StatusBadge";

type Props = {
  task: Task;
  layout: string;
};

export default function TaskCard({ task, layout }: Props) {
  return (
    <Link href={`/tasks/${task.id}`}>
      <div className={`${layout} px-4 py-4 border-b`}>
        <div className="flex items-center gap-4">
          <div className="flex flex-col">
            <span className="font-medium">{task.title}</span>
            <span className="text-xs line-clamp-1">{task.description}</span>
          </div>
        </div>

        <div className="flex justify-start">
          <StatusBadge status={task.status} />
        </div>

        <div className="text-sm">{task.priority}</div>
        <div className="text-sm">{task.due_date}</div>
        <div className="text-sm">{task.user_name}</div>
      </div>
    </Link>
  );
}
