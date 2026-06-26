"use client";

import { styles, circleStyles, completedCircleStyles } from "../styles";

type ActivityCardProps = {
  emoji: string;
  title: string;
  subtitle?: string;
  variant: "green" | "orange" | "teal";
  completed: boolean;
  onToggle: () => void;
};

export default function ActivityItem({
  emoji,
  title,
  subtitle,
  variant,
  completed,
  onToggle,
}: ActivityCardProps) {

  return (
    <div //layout
      className={`relative overflow-hidden flex min-h-25 items-center gap-4 rounded-[28px] border px-5 py-4 ${styles[variant]}`}
    >
      <div //แถบสี success
        className={`absolute left-0 top-0 h-full transition-[width] duration-500 ${
          completed ? "w-full" : "w-0"
        } ${completedCircleStyles[variant]}`}
      />

      <div className="relative z-10 text-4xl">{emoji}</div> 

      <div //Title + Subtitle
      className="relative z-10 flex-1">
        <div className="text-xl font-bold">{title}</div>

        {subtitle && (
          <div className="mt-1 text-base text-white/80">{subtitle}</div>
        )}
      </div>

      <button
        onClick={onToggle}
        className={`relative z-10 grid h-12 w-12 place-items-center rounded-full border-5 transition-all duration-500
          ${completed ? completedCircleStyles[variant] : circleStyles[variant]}`}
      >
        {completed && <span className="text-2xl font-bold text-white">✓</span>}
      </button>
    </div>
  );
}