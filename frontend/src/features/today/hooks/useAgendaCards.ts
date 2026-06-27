import { useState } from "react";
import { events, tasks } from "../lib/mockActivities";
import type { ActivityCard, ViewMode } from "../lib/type";
import { filterItemsByMode } from "./ActivityFilters";

const initialCards = (mode: ViewMode): ActivityCard[] => [
  {
    title: "Events",
    emoji: "📆",
    variant: "green",
    items: filterItemsByMode(
      events.map((item) => ({
        ...item,
        completed: false,
      })),
      mode
    ),
  },
  {
    title: "Tasks",
    emoji: "📋",
    variant: "teal",
    items: filterItemsByMode(
      tasks.map((item) => ({
        ...item,
        completed: false,
      })),
      mode
    ),
  },
];

export function useAgendaCards() {
  const [cards, setCards] = useState<ActivityCard[]>(initialCards("today")); //  set default today card

  // function(mode) -> card's object, item align by mode
  function getCardsByMode(mode: ViewMode): ActivityCard[] {
    return cards.map((card) => ({
      ...card,
      items: filterItemsByMode(card.items, mode),
    }));
  }

  // toggle complete item status
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
    getCardsByMode,
    toggleItem,
  };
}