import { TaskListProvider } from "@/src/contexts/TaskListContent";

export default function TasksLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <TaskListProvider>{children}</TaskListProvider>;
}
