import { TaskStatus } from "../types/task";

type Props = {
  status: TaskStatus;
  className?: string;
};

const statusConfig = {
  未着手: {
    label: "未着手",
    className: "bg-slate-100 text-slate-600",
  },
  対応中: {
    label: "対応中",
    className: "bg-blue-100 text-blue-700",
  },
  完了: {
    label: "完了",
    className: "bg-green-100 text-green-700",
  },
};

export default function StatusBadge({ status, className }: Props) {
  const config = statusConfig[status];

  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium w-20",
        config.className,
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <span className="mr-1.5 h-1.5 w-1.5 rounded-full bg-current" />
      {config.label}
    </span>
  );
}
