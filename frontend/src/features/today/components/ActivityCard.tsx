"use client";

import ActivityItem from "./ActivityItem";
import ProgressCircle from "./ProgressCircle";
import { useActivityCards } from "../hooks/useActivityCards";
import { useState } from "react";

export default function ActivityCard() {
  const { cards, toggleItem } = useActivityCards();
  const [openCards, setOpenCards] = useState<Record<string, boolean>>({});;

  function toggleCard(cardTitle: string) {
    setOpenCards((prev) => ({
      ...prev,
      [cardTitle]: !(prev[cardTitle] ?? true),
    }));
  }

  return (
    <div>
      {cards.map((card) => {
        const total = card.items.length;
        const current = card.items.filter((item) => item.completed).length;
        const isOpen = openCards[card.title] ?? true;

        return (
          <section
            key={card.title}
            className="rounded-[28px] border border-white/10 bg-zinc-900/90 p-3 shadow-lg mb-4"
          >
            <div className="mb-3 flex items-center justify-between px-1">
              <div className="text-sm font-bold text-white/80">
                {card.emoji} {card.title}
              </div>

              <ProgressCircle current={current} total={total} onToggle={() => toggleCard(card.title)} isOpen={isOpen}/>
            </div>

          {isOpen && (
            <div className="space-y-3">
              {card.items.map((item) => (
                <ActivityItem
                  key={item.id}
                  emoji={card.emoji}
                  title={item.title}
                  subtitle={item.due_date}
                  variant={card.variant}
                  completed={item.completed}
                  onToggle={() => toggleItem(card.title, item.id)}
                />
              ))}
            </div>
          )}
          </section>
        );
      })}
    </div>
  );
}