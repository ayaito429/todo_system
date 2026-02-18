type Props = {
  todo: number;
  inProgress: number;
  done: number;
};
const COLORS = {
  todo: "#94a3b8",
  inProgress: "#3b82f6",
  done: "#22c55e",
};

export function ProgressChart({ todo, inProgress, done }: Props) {
  const total = todo + inProgress + done;

  if (total === 0) {
    return (
      <div className="flex items-center gap-6 rounded-lg border p-4">
        <div className="h-32 w-32 rounded-full border-2 border-gray-200">
          <p className="text-sm text-gray-500">タスクがありません</p>
        </div>
      </div>
    );
  }

  const todoPercent = (todo / total) * 100;
  const inProgressPercent = (inProgress / total) * 100;
  const donePercent = (done / total) * 100;

  const p1 = todoPercent;
  const p2 = todoPercent + inProgressPercent;

  const gradient = `conic-gradient(
  ${COLORS.todo} 0% ${p1}%,
  ${COLORS.inProgress} ${p1}% ${p2}%,
  ${COLORS.done} ${p2}% 100%
  )`;

  return (
    <div className="flex flex-wrap items-center gap-6 rounded-lg border bg-white p-4 justify-center mb-10">
      <div className="relative h-32 w-32 flex-shrink-0">
        <div
          className="h-full w-full rounded-full"
          style={{ background: gradient }}
        >
          <div className="absolute left-1/2 top-1/2 h-20 w-20 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white" />
          <div className="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 flex-col items-center justify-center">
            <span className="text-xl font-bold">
              {Math.round(donePercent)}%
            </span>
            <span>完了</span>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2">
          <span
            className="h-3 w-3 rounded-full"
            style={{ backgroundColor: COLORS.todo }}
          />
          <span className="text-sm"> 未着手: {todo}件</span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className="h-3 w-3 rounded-full"
            style={{ backgroundColor: COLORS.inProgress }}
          />
          <span className="text-sm">対応中: {inProgress}件</span>
        </div>
        <div className="flex items-center gap-2">
          <span
            className="h-3 w-3 rounded-full"
            style={{ backgroundColor: COLORS.done }}
          />
          <span className="text-sm">完了: {done}件</span>
        </div>
      </div>
    </div>
  );
}
