"use client";
import { useRouter } from "next/navigation";
import {useState} from "react";
import { createTask } from "@/src/lib/api/tasks";
import { TaskPriority, TaskStatus } from "../types/task";



export default function NewTaskModal() {
  const [title,setTitle] = useState("");
  const [description,setDescription] = useState("");
  const [due_date,setDueDate] = useState("");
  const [priority,setPriority] = useState<TaskPriority>(1);
  const [user_id,setUserId] = useState(0);
  const [status,setStatus] = useState<TaskStatus>("未着手");
  const [ispublic,setPublic] = useState("");
  // const [created_by,setCreatedBy] = useState("");
  // const [updated_by,setUpdatedBy] = useState("");
  const router = useRouter();
  
  
  
  const handleCreate = async () => {
    try {
      await createTask({
   title: title,
   description: description,
   due_date: due_date,
   priority: priority,
   user_id: user_id,
   status: status,
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
      <label htmlFor="">タスク名</label>
      <input type="text" className="border 2px solid #333 bg-white padding-16px border-radius-6px" height={44} value={title} onChange={(e) => setTitle(e.target.value)}
      />
      <label htmlFor="">詳細説明</label>
      <input type="text" className="border 2px solid #333 bg-white padding-16px border-radius-6px" height={44} value={description} onChange={(e) => setDescription(e.target.value)}/>
      <label htmlFor="期限">期限</label>
      <input type="date" className="border 2px solid #333 bg-white padding-16px border-radius-6px" height={44} value={due_date} onChange={(e) => setDueDate(e.target.value)}/>
      <label htmlFor="優先度">優先度</label>
      <select name="" id="" value={priority} onChange={(e) => setPriority(Number(e.target.value)as TaskPriority)}>
        <option value="1">高</option>
        <option value="2">中</option>
        <option value="3">低</option>
      </select>
      <label htmlFor="担当者">担当者</label>
      <select name="" id="" value={user_id} onChange={(e) => setUserId(Number(e.target.value))}>
        <option value="1">田中</option>
        <option value="2">佐藤</option>
        <option value="3">山田</option>
      </select>
      <div>
      <label htmlFor="公開設定">公開設定</label>
      <input type="radio" name="公開設定" id="公開" value={ispublic} onChange={(e) => setPublic(e.target.value)}/>
      <label htmlFor="公開">公開</label>
      <input type="radio" name="公開設定" id="非公開" value={ispublic} onChange={(e) => setPublic(e.target.value)}/>
      <label htmlFor="非公開">非公開</label>
      </div>
      <div>
      <label htmlFor="ステータス">ステータス</label>
      <input type="radio" name="ステータス" id="未着手" value="未着手" checked={status === "未着手"} onChange={(e) => setStatus(e.target.value as TaskStatus)}/>
      <label htmlFor="未着手">未着手</label>
      <input type="radio" name="ステータス" id="対応中" value="対応中" checked={status === "対応中"} onChange={(e) => setStatus(e.target.value as TaskStatus)}/>
      <label htmlFor="対応中">対応中</label>
      <input type="radio" name="ステータス" id="完了" value="完了" checked={status === "完了"} onChange={(e) => setStatus(e.target.value as TaskStatus)}/>
      <label htmlFor="完了">完了</label>
      </div>      
      <button onClick={handleCreate}>作成</button>
      <button onClick={() => router.push("/tasks")}>閉じる</button>
    </div>
  );
}