import { useState } from "react";
import { events, tasks } from "../lib/mockActivities"; 
import type { ActivityCard, ViewMode } from "../lib/type";
import { filterItemsByMode } from "./ActivityFilters";

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

function formatCardDate(dueDate: string) {
  return new Date(dueDate).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function useAgendaCards() {
  const [cards, setCards] = useState<ActivityCard[]>(initialCards); //  set default today card

  // function(mode) -> card's object, item align by mode
  function getDateKey(dueDate: string) {
    const date = new Date(dueDate);

    return date.toISOString().split("T")[0];
  }

  function getCardsByMode(mode: ViewMode): ActivityCard[] {
    const filteredCards = cards.map((card) => ({
      ...card,
      items: filterItemsByMode(card.items, mode),
    }));

    if (mode === "today") {
      return filteredCards;
    }

    const allItems = filteredCards.flatMap((card) => card.items);

    const groupedByDate = allItems.reduce<Record<string, typeof allItems>>(
      (groups, item) => {
        const dateKey = getDateKey(item.due_date);

        if (!groups[dateKey]) {
          groups[dateKey] = [];
        }

        groups[dateKey].push(item);

        return groups;
      },
      {}
    );

    return Object.entries(groupedByDate).map(([dateKey, items]) => ({
      title: formatCardDate(dateKey),
      emoji: mode === "upcoming" ? "📅" : "⚠️",
      variant: mode === "upcoming" ? "green" : "teal",
      items,
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