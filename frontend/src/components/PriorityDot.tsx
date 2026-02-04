type Props = {
  priority: 1 | 2 | 3;
};

export default function PriorityDot({ priority }: Props) {
  const colors = {
    1: "bg-[#ef4444]", // 高:赤
    2: "bg-[#f59e0b]", // 中:黄
    3: "bg-[#10b981]", // 低:緑
  };

  return (
    <div
      className={`w-2.5 h-2.5 rounded-full border-2 border-[#333] shrink-0 ${colors[priority]}`}
    ></div>
  );
}
