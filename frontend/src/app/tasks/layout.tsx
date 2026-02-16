import { Header } from "@/src/components/Header";
import { TaskListProvider } from "@/src/contexts/TaskListContent";

export default function TasksLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <TaskListProvider>
      <Header />
      {children}
    </TaskListProvider>
  );
}
