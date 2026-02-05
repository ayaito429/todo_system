"use client";
import { useRouter } from "next/navigation";
import {useState} from "react";

export default function NewTaskModal() {
  const [title,setTitle] = useState("");
  // const [description,setDescription] = useState("");
  // const [due_date,setDueDate] = useState("");
  // const [priority,setPriority] = useState("");
  // const [user_id,setUserId] = useState("");
  // const [status,setStatus] = useState("");
  // const [public,setPublic] = useState("");
  // const [created_by,setCreatedBy] = useState("");
  // const [updated_by,setUpdatedBy] = useState("");
    const router = useRouter();
  return (
    <div>
      <h2>新規タスク作成</h2>
      <label htmlFor="">タスク名</label>
      <input type="text" className="border 2px solid #333 bg-white padding-16px border-radius-6px" height={44} value={title} onChange={(e) => setTitle(e.target.value)}
      />
      <label htmlFor="">詳細説明</label>
      <input type="text" className="border 2px solid #333 bg-white padding-16px border-radius-6px" height={44}/>
      <label htmlFor="期限">期限</label>
      <input type="date" className="border 2px solid #333 bg-white padding-16px border-radius-6px" height={44}/>
      <label htmlFor="優先度">優先度</label>
      <select name="" id="">
        <option value="1">高</option>
        <option value="2">中</option>
        <option value="3">低</option>
      </select>
      <label htmlFor="担当者">担当者</label>
      <select name="" id="">
        <option value="1">田中</option>
        <option value="2">佐藤</option>
        <option value="3">山田</option>
      </select>
      <div>
      <label htmlFor="公開設定">公開設定</label>
      <label htmlFor="公開">公開</label>
      <input type="radio" name="公開設定" id="公開" />
      <label htmlFor="非公開">非公開</label>
      <input type="radio" name="公開設定" id="非公開" />
      </div>
      <div>
      <label htmlFor="ステータス">ステータス</label>
      <label htmlFor="高">高</label>
      <input type="radio" name="ステータス" id="高" />
      <label htmlFor="非">中</label>
      <input type="radio" name="ステータス" id="中" />
      <label htmlFor="">低</label>
      <input type="radio" name="ステータス" id="低" />
      </div>      
      <button onClick={() => router.push("/tasks")}>作成</button>
      <button onClick={() => router.push("/tasks")}>閉じる</button>
    </div>
  );
}