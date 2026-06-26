
import { circleStyles, completedCircleStyles, type Variant,} from "../styles";

type ProgressCircleProps = {
  current: number;
  total: number;
  variant: Variant;
  onClick?: () => void;
};

export default function ProgressCircle({
  current,
  total,
  variant,
  onClick,
}: ProgressCircleProps) {
  const percent = total === 0 ? 0 : (current / total) * 100;
  const completed = current >= total;

  return (
    <button
      onClick={onClick}
      className={`relative grid h-12 w-12 overflow-hidden rounded-full border-5 transition-all duration-500 ${
        completed ? completedCircleStyles[variant] : circleStyles[variant]
      }`}
    >
      <div
        className={`absolute bottom-0 left-0 w-full transition-[height] duration-500 ${fillStyles[variant]}`}
        style={{ height: `${percent}%` }}
      />

      <span className="relative z-10 text-xl font-bold text-white">
        {completed ? "✓" : ""}
      </span>
    </button>
  );
}