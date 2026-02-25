"use client";
import NewTaskModal from "@/src/components/NewTaskModal";
import { useTaskList } from "@/src/contexts/TaskListContent";

export default function TaskNewPage() {
  const  users  = useTaskList();
  return (
    <div>
      <NewTaskModal users={users.users} />
    </div>
  );
}
