"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { createTask, deleteTask, updateTask } from "@/src/lib/api/tasks";
import { Task, TaskPriority, TaskStatus } from "../types/task";
import StatusBadge from "./StatusBadge";
import { ArrowLeft, Trash2 } from "lucide-react";
import { useUser } from "../contexts/UserContext";
import { User } from "../types/user";

type Props = {
  task?: Task;
  mode?: "create" | "view" | "edit";
  onClose?: () => void;
  users: User[];
};
function formatDateOnly(isoString: string | undefined): string {
  if (!isoString) return "-";
  return isoString.slice(0, 10);
}

export default function NewTaskModal({ task, mode, onClose, users }: Props) {
  console.log("users", users);
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [due_date, setDueDate] = useState(task?.due_date || "");
  const [priority, setPriority] = useState<TaskPriority>(
    task?.priority || "高",
  );
  const [status, setStatus] = useState<TaskStatus>(task?.status || "未着手");
  const [currentMode, setCurrentMode] = useState<"create" | "view" | "edit">(
    mode ?? (task ? "view" : "create"),
  );

  const router = useRouter();
  const isView = currentMode === "view";
  const isEdit = currentMode === "edit";
  const isCreate = currentMode === "create";

  const isFormMode = isCreate || isEdit;

  const [errors, setErrors] = useState<{
    title?: string;
    description?: string;
    due_date?: string;
  }>({});
  const { user } = useUser();

  const [user_id, setUserId] = useState(() => {
    if (task?.user_id != null) return task.user_id;
    if (user?.role === "user" && user?.user_id != null) return user.user_id;
    if (users?.length) return users[0].id ?? 0;
    return 0;
  });

  const canDelete =
    user != null && (user.role === "admin" || user.role === "leader");

  const canEdit =
    user != null &&
    (user.role === "admin" ||
      user.role === "leader" ||
      (user.role === "user" && task != null && task.user_id === user.user_id));

  const validateCreate = (): boolean => {
    const next: { title?: string; description?: string; due_date?: string } =
      {};
    if (!title.trim()) next.title = "タスク名を入力して下さい";
    if (!description.trim()) next.description = "詳細説明を入力して下さい";
    if (!due_date.trim()) next.due_date = "期限を入力して下さい";
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleCreate = async () => {
    if (!validateCreate()) return;
    try {
      await createTask({
        title: title,
        description: description,
        status: status,
        priority: priority,
        due_date: due_date,
        user_id: user_id,
        login_user: user?.user_id ?? 0,
        //  ispublic: ispublic,
      });

      router.push("/tasks");
    } catch (error) {
      console.error(error);
    }
  };

  const handleUpdate = async () => {
    if (!task?.id) return;
    try {
      await updateTask(task?.id, {
        title: title,
        description: description,
        status: status,
        priority: priority,
        due_date: due_date,
        user_id: user_id,
        login_user: 1,
      });
      router.push("/tasks");
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async () => {
    if (!task?.id) return;
    if (!window.confirm("タスクを削除しますか？")) return;
    try {
      await deleteTask(task?.id);
      router.push("/tasks");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className=" px-30 pt-5">
      <button
        type="button"
        onClick={() => router.push("/tasks")}
        className="mb-6 flex items-center gap-2 text-sm  hover:text-foreground"
      >
        <ArrowLeft className="h-4 w-4" />
        タスク一覧に戻る
      </button>
      <div className="border rounded-lg px-10 py-6 bg-white">
        {isFormMode ? (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (isCreate) handleCreate();
              else handleUpdate();
            }}
          >
            <div className="flex flex-col mb-5">
              <label htmlFor="task-title">タスク名</label>
              <input
                id="task-title"
                type="text"
                readOnly={isView}
                className="border-2 border-gray-200 bg-white p-4 rounded h-10 mb-5"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
              {errors.title && (
                <p className="text-red-600 text-sm mt-1">{errors.title}</p>
              )}
              <label htmlFor="task-description">詳細説明</label>
              <textarea
                id="task-description"
                rows={4}
                readOnly={isView}
                className="border-2 border-gray-200 bg-white p-4 rounded"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
              {errors.description && (
                <p className="text-red-600 text-sm mt-1">
                  {errors.description}
                </p>
              )}
            </div>
            <div className="grid grid-cols-1 gap-4 border-b border-gray-200 mb-5 sm:grid-cols-4 ">
              <div className="flex flex-col">
                <label htmlFor="status">ステータス</label>
                <select
                  name=""
                  id=""
                  value={status}
                  disabled={isView}
                  onChange={(e) => setStatus(e.target.value as TaskStatus)}
                  className="border border-gray-200 rounded w-23 px-3 py-2"
                >
                  <option value="未着手">未着手</option>
                  <option value="対応中">対応中</option>
                  <option value="完了">完了</option>
                </select>
              </div>
              <div>
                <label htmlFor="task-priority">優先度</label>
                <select
                  id="task-priority"
                  value={priority}
                  disabled={isView}
                  onChange={(e) => setPriority(e.target.value as TaskPriority)}
                  className="flex border border-gray-200 w-23 px-3 py-2 rounded"
                >
                  <option value="高">高</option>
                  <option value="中">中</option>
                  <option value="低">低</option>
                </select>
              </div>
              <div className="">
                <label htmlFor="task-due-date">期限</label>
                <input
                  id="task-due-date"
                  type="date"
                  readOnly={isView}
                  className="border border-gray-200 bg-white p-4 rounded h-10 flex"
                  value={due_date}
                  onChange={(e) => setDueDate(e.target.value)}
                />
                {errors.due_date && (
                  <p className="text-red-600 text-sm mt-1">{errors.due_date}</p>
                )}
              </div>
              <div className="justify-between">
                <label htmlFor="task-user-id">担当者</label>
                {user?.role === "user" ? (
                  <div
                    id="task-user-id"
                    className="border border-gray-200 rounded px-3 py-2 bg-gray-100 text-gray-700"
                  >
                    {user.name}
                  </div>
                ) : (
                  <select
                    id="task-user-id"
                    value={user_id}
                    disabled={isView}
                    onChange={(e) => setUserId(Number(e.target.value))}
                    className="border border-gray-200 rounded px-3 py-2 w-full"
                  >
                    {users?.length ? (
                      users
                        .filter((u) => u.role !== "admin")
                        .map((u) => (
                          <option key={u.id} value={u.id}>
                            {u.name}
                          </option>
                        ))
                    ) : (
                      <option value={0}>-</option>
                    )}
                  </select>
                )}
              </div>
            </div>
            <div className="flex justify-between items-center">
              {isEdit && task && canDelete ? (
                <button
                  type="button"
                  onClick={handleDelete}
                  className="text-red-300 flex hover:bg-red-100 rounded px-2 py-1"
                >
                  <Trash2 className="text-red-300" />
                  削除
                </button>
              ) : (
                <div />
              )}
              <div className="flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={onClose || (() => router.push("/tasks"))}
                  className="border border-gray-300 rounded px-4 py-2 hover:bg-gray-50"
                >
                  キャンセル
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 text-white rounded px-4 py-2 hover:bg-blue-600"
                >
                  {isCreate ? "作成" : "保存"}
                </button>
              </div>
            </div>
          </form>
        ) : (
          <>
            <div className="px-10 py-6">
              <div className="flex justify-between border-b border-gray-200">
                <h1 className="text-xl font-semibold text-gray-900 mb-4">
                  {title}
                </h1>

                <div className="ml-4 flex items-center gap-2">
                  {canEdit && (
                    <button
                      type="button"
                      onClick={() => setCurrentMode("edit")}
                      className="border border-gray-200 rounded px-3 py-1 mr-2"
                    >
                      編集
                    </button>
                  )}
                </div>
              </div>
              <div>
                <h2 className="text-sm font-medium text-gray-500 mt-5">
                  詳細説明
                </h2>
                <p className="text-gray-900">
                  {description || "説明がありません"}
                </p>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg mb-4 border border-gray-200 ">
                <div>
                  <p className="text-xs font-medium text-gray-500 mb-1">
                    ステータス
                  </p>
                  <StatusBadge status={status} />
                </div>
                <div>
                  <p className="text-xs font-medium text-gray-500 mb-1">
                    優先度
                  </p>
                  <p className="text-sm">{priority}</p>
                </div>
                <div>
                  <p className="text-xs font-medium text-gray-500">期限</p>
                  <p>{due_date}</p>
                </div>
                <div>
                  <p className="text-xs font-medium text-gray-500 mb-1">
                    担当者
                  </p>
                  <p>{task?.user_name}</p>
                </div>
              </div>

              <div className="text-xs text-gray-500 border-t border-gray-200 pt-4 mb-4">
                <span>作成日:{formatDateOnly(task?.created_at)}</span>
                <span className="mx-2">|</span>
                <span>最終更新:{formatDateOnly(task?.updated_at)}</span>
                <span className="mx-2">|</span>
                <span>作成者:{task?.created_name}</span>
                <span className="mx-2">|</span>
                <span>更新者:{task?.updated_name}</span>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
