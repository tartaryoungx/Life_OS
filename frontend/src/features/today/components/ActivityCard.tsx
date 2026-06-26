import ActivityItem from "./ActivityItem";
import { events, tasks } from "../data/mockActivities";

const cards = [
  {
    title: "Events",
    emoji: "📆",
    variant: "green",
    items: events,
  },
  {
    title: "Tasks",
    emoji: "📋",
    variant: "teal",
    items: tasks,
  },
] as const;

export default function ActivityCard() {
  return (
    <div className="space-y-4">
      {cards.map((card) => (
        <section
          key={card.title}
          className="rounded-[28px] border border-white/10 bg-zinc-900/90 p-3 shadow-lg"
        >
          <div className="mb-3 flex items-center justify-between px-1">
            <div className="text-sm font-bold text-white/80">
              {card.emoji} {card.title}
            </div>

            <button className="grid h-10 w-10 place-items-center rounded-full border-[5px] border-yellow-400/80">
              ▲
            </button>
          </div>

          <div className="space-y-3">
            {card.items.map((item) => (
              <ActivityItem
                key={item.id}
                emoji={card.emoji}
                title={item.title}
                subtitle={item.due_date}
                variant={card.variant}
              />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}