"use client";

type ViewToggleProps = {
  view: "list" | "map";
  setView: (v: "list" | "map") => void;
};

export default function ViewToggle({ view, setView }: ViewToggleProps) {
  return (
    <div className="flex gap-2 mb-4">
      <button
        onClick={() => setView("list")}
        className={`px-4 py-2 rounded ${view === "list" ? "bg-cyan-500 text-black" : "bg-gray-700 text-white"}`}
      >
        List View
      </button>
      <button
        onClick={() => setView("map")}
        className={`px-4 py-2 rounded ${view === "map" ? "bg-cyan-500 text-black" : "bg-gray-700 text-white"}`}
      >
        Map View
      </button>
    </div>
  );
}
