import Header from "../../../components/layout/Header";
import type { ViewMode } from "../lib/type";
import { labels } from "../lib/type";

type TodayHeaderProps = {
  mode: ViewMode; //object : "overdue" | "today" | "upcoming";
};

export default function TodayHeader({ mode }: TodayHeaderProps) {
  return <Header title={labels[mode]} />;
}