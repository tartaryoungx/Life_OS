"use client";

import TodayHeader from "./components/TodayHeader";
import ActivityCard from "./components/ActivityCard";
import BottomNav from "../../components/layout/BottomNav";
import { useSwipeMode } from "./hooks/useSwipeMode";

export default function Today() {
  const {
    mode,
    modes,
    changeMode,
    handleTouchStart,
    handleTouchEnd,
  } = useSwipeMode();

  return (
    <main className="h-dvh overflow-hidden bg-black text-white">

      {/* swipe */}
      <div
        className="mx-auto flex h-full w-full max-w-md flex-col md:max-w-7xl"
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      > 
        {/* Header */}
        <div className="sticky top-0 z-50 bg-black px-4 py-8 md:px-8">
          <TodayHeader mode={mode} />
        </div> 

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-4 md:px-8">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="mt-4">
              <ActivityCard mode={mode} /> {/* Card+Item */}
            </div>
          </div>
        </div>

        {/* Mode Buttons */}
        <div className="bg-black px-4 pt-3">
          <div className="flex justify-center gap-3">
            {modes.map((item) => (
              <button
                key={item}
                onClick={() => changeMode(item)}
                className={`rounded-full px-4 py-2 text-sm capitalize transition ${
                  mode === item
                    ? "bg-white text-black"
                    : "bg-zinc-800 text-zinc-400"
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>
        
        {/* Bottom Nav */}
        <div className="sticky bottom-0 z-50 bg-black px-4 pt-3 pb-6 md:px-8">
          <BottomNav /> 
        </div>
      </div>
    </main>
  );
}