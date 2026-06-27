"use client";

type ViewMode = "overdue" | "today" | "upcoming";

type TopBarProps = {
  mode: ViewMode;
  setMode: (mode: ViewMode) => void;
};

const modes: ViewMode[] = ["overdue", "today", "upcoming"];

const labels: Record<ViewMode, string> = {
  overdue: "Overdue",
  today: "Today",
  upcoming: "Upcoming",
};

export default function TopBar({ mode, setMode }: TopBarProps) {
  return (
    <header className="flex items-center justify-between">
      <div className="w-16" />

      <div className="flex flex-col items-center gap-2">
        <h1 className="text-2xl font-bold">{labels[mode]}</h1>

        <div className="flex items-center gap-2">
          {modes.map((item) => (
            <button
              key={item}
              onClick={() => setMode(item)}
              className={`h-2.5 rounded-full transition-all duration-300 ${
                mode === item
                  ? "w-6 bg-white"
                  : "w-2.5 bg-zinc-600 hover:bg-zinc-400"
              }`}
              aria-label={`Show ${labels[item]}`}
            />
          ))}
        </div>
      </div>

      <button className="grid h-16 w-16 place-items-center rounded-full bg-indigo-500 text-5xl font-light">
        +
      </button>
    </header>
  );
}