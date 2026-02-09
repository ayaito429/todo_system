import Link from "next/link";
import { Task } from "../types/task";
import PriorityDot from "./PriorityDot";
import StatusBadge from "./StatusBadge";

type Props = {
  task: Task;
  onClick: () => void;
};

export default function TaskCard({ task ,onClick}: Props) {
  return (
          <tr key={task.id} onClick={onClick}>
            <td>
              <p>{task.title}</p>
              <p>{task.description}</p>
              </td>
            <td>{task.status}</td>
            <td>{task.priority}</td>
            <td>{task.due_date}</td>
            <td>{task.user.name}</td>
          </tr>
       
  );
}
