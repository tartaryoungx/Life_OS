import { useState } from "react";
import type { ViewMode } from "../lib/type";

const modes: ViewMode[] = ["overdue", "today", "upcoming"];

export function useSwipeMode() {
  const [mode, setMode] = useState<ViewMode>("today");
  const [touchStart, setTouchStart] = useState<number | null>(null);

  function handleTouchStart(e: React.TouchEvent) {
    setTouchStart(e.touches[0].clientX);
  }

  function handleTouchEnd(e: React.TouchEvent) {
    if (touchStart === null) return;

    const touchEnd = e.changedTouches[0].clientX;
    const diff = touchStart - touchEnd;
    const index = modes.indexOf(mode);

    if (diff > 100 && index < modes.length - 1) {
      setMode(modes[index + 1]);
    }

    if (diff < -100 && index > 0) {
      setMode(modes[index - 1]);
    }

    setTouchStart(null);
  }

  return {
    mode,
    handleTouchStart,
    handleTouchEnd,
  };
}