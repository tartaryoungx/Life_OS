import { useState } from "react";

export type ViewMode = "overdue" | "today" | "upcoming";

const modes: ViewMode[] = ["overdue", "today", "upcoming"];

export function useSwipeMode(initialMode: ViewMode = "today") {
  const [mode, setMode] = useState<ViewMode>(initialMode);
  const [touchStart, setTouchStart] = useState<number | null>(null);

  function handleTouchStart(e: React.TouchEvent) {
    setTouchStart(e.touches[0].clientX);
  }

  function handleTouchEnd(e: React.TouchEvent) {
    if (touchStart === null) return;

    const touchEnd = e.changedTouches[0].clientX;
    const diff = touchStart - touchEnd;
    const index = modes.indexOf(mode);

    if (diff > 50 && index < modes.length - 1) {
      setMode(modes[index + 1]);
    }

    if (diff < -50 && index > 0) {
      setMode(modes[index - 1]);
    }

    setTouchStart(null);
  }

  return {
    mode,
    setMode,
    handleTouchStart,
    handleTouchEnd,
  };
}