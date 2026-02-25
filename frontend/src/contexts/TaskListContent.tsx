"use client";
import { createContext, useContext, useState, ReactNode } from "react";
import { Task } from "../types/task";
import { User } from "../types/user";

type TaskListContextType = {
  tasks: Task[];
  setTasks: (tasks: Task[]) => void;
  team_name: string;
  setTeamName: (name: string) => void;
  users: User[];
  setUsers: (users: User[]) => void;
};

const TaskListContext = createContext<TaskListContextType | null>(null);

export function useTaskList() {
  const ctx = useContext(TaskListContext);
  if (!ctx) throw new Error("useContextが使用できませんでした");
  return ctx;
}

export function TaskListProvider({ children }: { children: ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [team_name, setTeamName] = useState<string>("");
  const [users, setUsers] = useState<User[]>([]);
  return (
    <TaskListContext.Provider
      value={{ tasks, setTasks, team_name, setTeamName, users, setUsers }}
    >
      {children}
    </TaskListContext.Provider>
  );
}
