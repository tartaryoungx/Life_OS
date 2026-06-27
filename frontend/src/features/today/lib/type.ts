
export type Variant = "green" | "orange" | "teal";

export type Activity = {
  id: string;
  title: string;
  due_date: string;
  completed: boolean;
};

export type ActivityCard = {
  title: string;
  emoji: string;
  variant: Variant;
  items: Activity[];
};

export type ModeProps = {
  mode: ViewMode;
};

// Header 
export type ViewMode = "overdue" | "today" | "upcoming";

export const labels: Record<ViewMode, string> = {
  overdue: "Overdue",
  today: "Today",
  upcoming: "Upcoming",
};