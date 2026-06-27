"use client";

import TopBar from "../../components/layout/TopBar";
import DateStrip from "../../features/today/components/DateStrip";
import ActivityCard from "../../features/today/components/ActivityCard";
import BottomNav from "../../components/layout/BottomNav";
import { useState } from "react";

type ViewMode = "overdue" | "today" | "upcoming";

export default function Today() {
  const [mode, setMode] = useState<ViewMode>("today");
  const modes: ViewMode[] = ["overdue", "today", "upcoming"];

  const [touchStart, setTouchStart] = useState<number | null>(null);

  function handleTouchStart(e: React.TouchEvent) {
  setTouchStart(e.touches[0].clientX);
  }

  function handleTouchEnd(e: React.TouchEvent) {
    if (touchStart === null) return;

    const touchEnd = e.changedTouches[0].clientX;
    const diff = touchStart - touchEnd;

    const index = modes.indexOf(mode);

    // ปัดซ้าย
    if (diff > 50 && index < modes.length - 1) {
      setMode(modes[index + 1]);
    }

    // ปัดขวา
    if (diff < -50 && index > 0) {
      setMode(modes[index - 1]);
    }

    setTouchStart(null);
  }

  return (
    <main className="min-h-screen bg-black text-white">
      <div className="mx-auto flex flex-col min-h-screen w-full max-w-md px-4 pt-10 pb-6 md:max-w-7xl md:px-8" 
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      >
        <TopBar mode={mode} setMode={setMode} />

        {/* <DateStrip /> */}

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="mt-4">
            <ActivityCard />
          </div>
        </div>

        <div className="flex-1" />

        <BottomNav />
      </div>
    </main>
  );
}

