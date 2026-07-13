import { useState } from "react";
import { Nav } from "./components/Nav";
import { CompanyTab } from "./components/CompanyTab";
import type { Ticker } from "./types";

function App() {
  const [active, setActive] = useState<Ticker>("VRTX");

  return (
    <div className="min-h-screen bg-bg text-text">
      <Nav active={active} onSelect={setActive} />
      <main className="mx-auto max-w-6xl px-6 py-8">
        <CompanyTab ticker={active} />
      </main>
    </div>
  );
}

export default App;
