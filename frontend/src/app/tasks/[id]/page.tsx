import { notFound } from "next/navigation";
import TaskDetailView from "./TaskDetailView";

export default async function TaskDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const numericId = Number(id);

  if (Number.isNaN(numericId)) {
    notFound();
  }
  return (
    <div className="px-20 pt-10">
      <TaskDetailView />
    </div>
  );
}
