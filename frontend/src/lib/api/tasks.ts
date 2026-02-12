// import { Task , TaskCreate } from "@/src/types/task";
import { apiClient } from "./client";

// // タスク一覧取得
// export async function getTasks():Promise<Task[]> {
//   const url = `${apiClient.baseUrl}/tasks`;
//   const res = await fetch(url);
//   if(!res.ok) {
//     throw new Error(`タスクが見つかりませんでした: ${res.status}`)
//     }
//     const data = await res.json();
//   return data as Task[];
// }

// タスク作成
export async function createTask(body: TaskCreate) {
  const url = `${apiClient.baseUrl}/api/tasks`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`タスク作成に失敗しました: ${res.status}`);
  }
  const data = await res.json();
  return data as Task;
}

// // タスク詳細取得
// export async function getTask(id: number):Promise<Task> {
//   const url = `${apiClient.baseUrl}/tasks/${id}`;
//   const res = await fetch(url,{
//     method: "GET",
//     headers: {
//       "Content-Type": "application/json"
//     }
// });
//   if(!res.ok) {
//     throw new Error(`タスクが見つかりませんでした: ${res.status}`)
//   }
//   return await res.json() as Task;
// }

// //タスク更新
export async function updateTask(id: number, body: TaskCreate) {
  const url = `${apiClient.baseUrl}/tasks/${id}`;
  const res = await fetch(url, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`タスクが更新できませんでした: ${res.status}`);
  }
  return (await res.json()) as Task;
}

// //タスクの削除
// export async function deleteTask(id:number) {
//   const url = `${apiClient.baseUrl}/tasks/${id}`
//   const res = await fetch(url,{
//     method: "DELETE",
//     headers: {
//       "Content-Type": "application/json"
//     }
//   });
//   if(!res.ok) {
//     throw new Error(`タスクが削除できませんでした: ${res.status}`)
//   }
//   return await res.json() as Task
// }

// lib/api/tasks.ts

import { Task, TaskCreate } from "@/src/types/task";
import { mockTasks } from "@/src/mocks/data/tasks"; // モックデータをインポート

// タスク一覧取得（モック版）
export async function getTasks(): Promise<Task[]> {
  console.log("Mock API: getTasks 実行");
  return new Promise((resolve) => {
    setTimeout(() => resolve(mockTasks), 500); // 0.5秒後にデータを返す
  });
}

// タスク詳細取得（モック版）
export async function getTask(id: number): Promise<Task> {
  console.log(`Mock API: getTask(${id}) 実行`);
  const task = mockTasks.find((t) => t.id === id);
  if (!task) throw new Error("Task not found");
  return task;
}

// タスク作成（モック版）
// export async function createTask(body: TaskCreate) {
//   console.log("Mock API: createTask 実行", body);
//   return { id: Math.floor(Math.random() * 1000), ...body } as Task;
// }
