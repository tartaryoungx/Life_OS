import type { Activity, ViewMode } from "../lib/type";

function isSameDate(a: Date, b: Date) {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

// function filter item by mode -> item array
export function filterItemsByMode(items: Activity[], mode: ViewMode) {
  const today = new Date();

  return items.filter((item) => {
    const due = new Date(item.due_date);

    if (mode === "today") {
      return isSameDate(due, today);
    }

    if (mode === "overdue") {
      return due < today && !isSameDate(due, today);
    }

    if (mode === "upcoming") {
      return due > today && !isSameDate(due, today);
    }

    return false;
  });
}