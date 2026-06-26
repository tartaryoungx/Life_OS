export type Item = {
  id: string;
  user_id: string;
  title: string;
  due_date: string;
};

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