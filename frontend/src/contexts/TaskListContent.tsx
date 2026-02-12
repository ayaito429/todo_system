"use client";
import { createContext, useContext, useState, ReactNode } from "react";
import { Task } from "../types/task";

type TaskListContextType = {
  tasks: Task[];
  setTasks: (tasks: Task[]) => void;
};

const TaskListContext = createContext<TaskListContextType | null>(null);

export function useTaskList() {
  const ctx = useContext(TaskListContext);
  if (!ctx) throw new Error("useContextが使用できませんでした");
  return ctx;
}

export function TaskListProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  return (
    <TaskListContext.Provider value={{ tasks, setTasks }}>
      {children}
    </TaskListContext.Provider>
  );
}
