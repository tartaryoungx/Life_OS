const days = [
  ["Sun", "21"],
  ["Mon", "22"],
  ["Tue", "23"],
  ["Wed", "24"],
  ["Thu", "25"],
  ["Fri", "26"],
  ["Sat", "27"],
];

export default function DateStrip() {
  return (
    <div className="mt-6 flex items-center justify-between">
      {days.map(([day, date]) => {
        const active = day === "Fri";

        return (
          <div key={day} className="flex flex-col items-center gap-2">
            <div className={active ? "font-bold text-white" : "text-zinc-500"}>
              {day}
            </div>

            <div
              className={
                active
                  ? "grid h-20 w-16 place-items-center rounded-full bg-indigo-500 text-xl font-bold"
                  : "grid h-10 w-10 place-items-center rounded-full border-4 border-indigo-950 text-zinc-500"
              }
            >
              {date}
            </div>
          </div>
        );
      })}
    </div>
  );
}