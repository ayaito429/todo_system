export default function TaskDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  return (
    <div>
      <h1>タスク詳細・編集</h1>
      {/* TODO: モーダル表示、params.id で取得 */}
    </div>
  );
}
