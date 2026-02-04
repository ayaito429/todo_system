import TaskCard from "@/src/components/TaskCard";
import { mockTasks } from "../../mocks/data/tasks";

export default function TaskListPage() {
  return (
    <div>
      <h1>タスク一覧</h1>
      <div>
        <div>
          <tr>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>担当者</th>
          </tr>
        </div>
        {mockTasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  );
}
