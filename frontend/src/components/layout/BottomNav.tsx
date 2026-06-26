const items = [
  ["▤", "Activity"],
  ["▥", "Statistics"],
  ["👥", "Sharing"],
  ["⚙", "Settings"],
];

export default function BottomNav() {
  return (
    <nav className="flex h-20 items-center justify-around rounded-full border border-zinc-800 bg-zinc-900 px-2">
      {items.map(([icon, label], index) => {
        const active = index === 0;

        return (
          <div
            key={label}
            className={
              active
                ? "flex h-16 w-28 flex-col items-center justify-center rounded-full bg-zinc-800 text-indigo-400"
                : "flex flex-col items-center justify-center text-white"
            }
          >
            <div className="text-3xl">{icon}</div>
            <div className="text-sm font-semibold">{label}</div>
          </div>
        );
      })}
    </nav>
  );
}