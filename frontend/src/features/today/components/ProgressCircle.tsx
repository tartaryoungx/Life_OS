type ProgressCircleProps = {
  current: number;
  total: number;
  onToggle: () => void;
  isOpen: boolean;
};

export default function ProgressCircle({
  current,
  total,
  onToggle,
  isOpen,
}: ProgressCircleProps) {
  const percent = total === 0 ? 0 : Math.min((current / total) * 100, 100);
  const degree = percent * 3.6;

  return (
    <button onClick={onToggle}>
    <div
      className="progress-ring relative grid h-10 w-10 place-items-center rounded-full"
      style={
        {
          "--progress": `${degree}deg`,
        } as React.CSSProperties
      }
    >
      <div className="absolute inset-1 rounded-full bg-zinc-900" />
      <span
        className={`relative z-10 text-sm font-bold text-white transition-transform duration-300 ${
            isOpen ? "rotate-0" : "rotate-180"
        }`}
        >
        ▲
      </span>
    </div>
    </button>
  );
}