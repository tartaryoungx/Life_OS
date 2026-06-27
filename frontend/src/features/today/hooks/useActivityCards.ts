import { useState } from "react";
import { events, tasks } from "../lib/mockActivities";
import type { ActivityCard } from "../lib/type";

const initialCards: ActivityCard[] = [
  {
    title: "Events",
    emoji: "📆",
    variant: "green",
    items: events.map((item) => ({
      ...item,
      completed: false,
    })),
  },
  {
    title: "Tasks",
    emoji: "📋",
    variant: "teal",
    items: tasks.map((item) => ({
      ...item,
      completed: false,
    })),
  },
];

export function useActivityCards() {
  const [cards, setCards] = useState<ActivityCard[]>(initialCards);

  function toggleItem(cardTitle: string, itemId: string) {
    setCards((prevCards) =>
      prevCards.map((card) =>
        card.title !== cardTitle
          ? card
          : {
              ...card,
              items: card.items.map((item) =>
                item.id === itemId
                  ? { ...item, completed: !item.completed }
                  : item
              ),
            }
      )
    );
  }

  return {
    cards,
    toggleItem,
  };
}