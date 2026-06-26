export default function TopBar() {
  return (
    <header className="flex items-center justify-between">
      <div className="flex h-14 w-32 items-center justify-around rounded-full border border-zinc-800 bg-zinc-900">
        <span className="text-3xl">☷</span>
        <span className="text-3xl">≡</span>
      </div>

      <h1 className="text-2xl font-bold">Today</h1>

      <button className="grid h-16 w-16 place-items-center rounded-full bg-indigo-500 text-5xl font-light">
        +
      </button>
    </header>
  );
}