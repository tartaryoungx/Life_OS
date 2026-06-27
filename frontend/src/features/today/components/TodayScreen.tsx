"use client";

import TopBar from "../../../components/layout/TopBar";
import ActivityCard from "../../../features/today/components/ActivityCard";
import BottomNav from "../../../components/layout/BottomNav";
import { useSwipeMode } from "../../../features/today/hooks/useSwipeMode";

export default function Today() {
  const { mode, setMode, handleTouchStart, handleTouchEnd } =
    useSwipeMode("today");

  return (
    <main className="h-dvh overflow-hidden bg-black text-white">
      <div
        className="mx-auto flex h-full w-full max-w-md flex-col overflow-y-auto px-4 md:max-w-7xl md:px-8"
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        <div className="sticky top-0 z-50 bg-black px-4 pt-10 pb-4 md:px-8">
          <TopBar mode={mode} setMode={setMode} />
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="mt-4">
            <ActivityCard />
          </div>
        </div>

        <div className="flex-1" />

        <div className="sticky bottom-0 z-50 bg-black px-4 pt-3 pb-6 md:px-8">
          <BottomNav />
        </div>
      </div>
    </main>
  );
}