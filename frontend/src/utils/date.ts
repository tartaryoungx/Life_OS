export function formatDueDate(dueDate: string) {
  const due = new Date(dueDate);
  const today = new Date();

  const isToday =
    due.getFullYear() === today.getFullYear() &&
    due.getMonth() === today.getMonth() &&
    due.getDate() === today.getDate();

  if (isToday) {
    return "Today";
  }

  return due.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}