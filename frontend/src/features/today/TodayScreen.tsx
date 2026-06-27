"use client";

import TodayHeader from "../today/components/TodayHeader";
import ActivityCard from "./components/ActivityCard";
import BottomNav from "../../components/layout/BottomNav";
import { useSwipeMode } from "./hooks/useSwipeMode";

export default function Today() {
  const { mode, handleTouchStart, handleTouchEnd } = useSwipeMode();

  return (
    <main className="h-dvh overflow-hidden bg-black text-white">
      <div
        className="mx-auto flex h-full w-full max-w-md flex-col md:max-w-7xl"
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        <div className="sticky top-0 z-50 bg-black px-4 py-8 md:px-8">
          <TodayHeader mode={mode} />
        </div>

        <div className="flex-1 overflow-y-auto px-4 md:px-8">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="mt-4">
              <ActivityCard />
            </div>
          </div>
        </div>

        <div className="sticky bottom-0 z-50 bg-black px-4 pt-3 pb-6 md:px-8">
          <BottomNav />
        </div>
      </div>
    </main>
  );
}