import TopBar from "../../components/layout/TopBar";
import DateStrip from "../../features/today/components/DateStrip";

import BottomNav from "../../components/layout/BottomNav";


export default function Timeline() {
  return (
    <main className="min-h-screen bg-black text-white">
      <div className="mx-auto flex flex-col min-h-screen w-full max-w-md px-4 pt-10 pb-6 md:max-w-7xl md:px-8">
        <TopBar />

        {/* <DateStrip /> */}

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="mt-4">

          </div>
        </div>

        <div className="flex-1" />

        <BottomNav />
      </div>
    </main>
  );
}
