"use client";

import ActivityItem from "./ActivityItem";
import ProgressCircle from "./ProgressCircle";
import { useAgendaCards } from "../hooks/useAgendaCards";
import { useState } from "react";
import type { ModeProps } from "../lib/type";

export default function ActivityCard({mode}: ModeProps) {
  const { toggleItem, getCardsByMode } = useAgendaCards(); // card
  const [openCards, setOpenCards] = useState<Record<string, boolean>>({});;
  const cards = getCardsByMode(mode);

  //เปิด ปิด card
  function toggleCard(cardTitle: string, isOpen: boolean) {
    setOpenCards((prev) => ({
      ...prev,
      [cardTitle]: !(isOpen), //เริ่มมาต้องปิดได้ เพราะ default เปิด
    }));
  }

  return (
    <div>
      {cards.map((card) => {
        const total = card.items.length;
        const current = card.items.filter((item) => item.completed).length;
        const isOpen = openCards[card.title] ?? true; // default open

        return (
          <section
            key={card.title}
            className="rounded-[28px] border border-white/10 bg-zinc-900/90 p-3 shadow-lg mb-4"
          >
            <div className="mb-3 flex items-center justify-between px-1">
              <div className="text-sm font-bold text-white/80">
                {card.emoji} {card.title}
              </div>

              <ProgressCircle current={current} total={total} 
              onToggle={() => toggleCard(card.title, isOpen)} isOpen={isOpen}/>
              {/* pass open value เข้าไปใช้ตอน onClick*/}
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