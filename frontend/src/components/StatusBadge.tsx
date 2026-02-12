import { TaskStatus } from "../types/task";

type Props = {
  status: TaskStatus;
};

export default function StatusBadge({ status }: Props) {
  const labels = {
    todo: "未着手",
    doing: "進行中",
    done: "完了",
  };
  return (
    <span className="px-2.5 py-0.75 border-2 border-[#333] rounded-md font-bold text-[11px] bg-white">
      {/* {labels[status]} */}
    </span>
  );
}
