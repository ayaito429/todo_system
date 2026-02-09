"use client";
import { useRouter } from "next/navigation";
import {useState} from "react";
import { createTask } from "@/src/lib/api/tasks";
import { Task, TaskPriority, TaskStatus } from "../types/task";

type Props = {
  task?: Task;
  onClose?: () => void;
}


export default function NewTaskModal({task, onClose}:Props) {
  const [title,setTitle] = useState(task?.title || "");
  const [description,setDescription] = useState(task?.description || "");
  const [due_date,setDueDate] = useState(task?.due_date || "");
  const [priority,setPriority] = useState<TaskPriority>(task?.priority || "高");
  const [user_id,setUserId] = useState(1);
  const [status,setStatus] = useState<TaskStatus>(task?.status || "未着手");
  const [ispublic,setPublic] = useState("");
  // const [created_by,setCreatedBy] = useState("");
  // const [updated_by,setUpdatedBy] = useState("");
  const router = useRouter();
  
  
  
  const handleCreate = async () => {
    try {
      await createTask({
   title: title,
   description: description,
   status: status,
   priority: priority,
   due_date: due_date,
   user_id: user_id,
   login_user: 1,
  //  ispublic: ispublic,
      });
      
      router.push("/tasks");
    }
    catch (error) {
      console.error(error);
    }
  }
  
  return (
    <div>
      <h2>新規タスク作成</h2>
      <div className="flex flex-col"> 
      <label htmlFor="task-title">タスク名</label>
      <input id="task-title" type="text" className="border-2 border-gray-800 bg-white p-4 rounded" height={44} value={title} onChange={(e) => setTitle(e.target.value)}
      />
      <label htmlFor="task-description">詳細説明</label>
      <input id="task-description" type="text" className="border-2 border-gray-800 bg-white p-4 rounded" height={44} value={description} onChange={(e) => setDescription(e.target.value)}/>
      </div>
      <div className="flex justify-between" >
        <div>
    <label htmlFor="status">ステータス</label>
      <input type="radio" name="status-todo" id="status-todo" value="未着手" checked={status === "未着手"} onChange={(e) => setStatus(e.target.value as TaskStatus)}/>
      <label htmlFor="status-todo">未着手</label>
      <input type="radio" name="status-todo" id="status-doing" value="対応中" checked={status === "対応中"} onChange={(e) => setStatus(e.target.value as TaskStatus)}/>
      <label htmlFor="status-doing">対応中</label>
      <input type="radio" name="status-todo" id="status-done" value="完了" checked={status === "完了"} onChange={(e) => setStatus(e.target.value as TaskStatus)}/>
      <label htmlFor="status-done">完了</label>
        </div>
        <div>
      <label htmlFor="task-priority">優先度</label>
      <select id="task-priority" value={priority} onChange={(e) => setPriority(e.target.value as TaskPriority)}>
        <option value="高">高</option>
        <option value="中">中</option>
        <option value="低">低</option>
      </select>
      </div>
      </div>
      <div className="flex flex-col">
      <label htmlFor="task-due-date">期限</label>
      <input id="task-due-date" type="date" className="border-2 border-gray-800 bg-white p-4 rounded" height={44} value={due_date} onChange={(e) => setDueDate(e.target.value)}/>
      </div>
      <div className="flex justify-between space-y-2">
      <label htmlFor="task-user-id">担当者</label>
      <select name="" id="task-user-id" value={user_id} onChange={(e) => setUserId(Number(e.target.value))}>
        <option value="1">田中</option>
        <option value="2">佐藤</option>
        <option value="3">山田</option>
      </select>
      <div>
      <label htmlFor="task-ispublic">公開設定</label>
      <input type="radio" name="公開設定" id="task-ispublic-public" value="public" checked={ispublic === "public"} onChange={(e) => setPublic(e.target.value)}/>
      <label htmlFor="task-ispublic-public">公開</label>
      <input type="radio" name="公開設定" id="task-ispublic-private" value="private" checked={ispublic === "private"} onChange={(e) => setPublic(e.target.value)}/>
      <label htmlFor="task-ispublic-private">非公開</label>
      </div>
      </div>
      <div>
        <span>作成:{task?.created_at}</span>
        <span>更新:{task?.updated_at}</span>
        <span>作成者:{task?.created_by}</span>
      </div>
      <button type="button" onClick={handleCreate}>作成</button>
      <button type="button" onClick={onClose || (() => router.push("/tasks"))
      }>閉じる</button>
    </div>
  );
}