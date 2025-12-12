
import { FaMap, FaList } from "react-icons/fa";
interface ViewToggleProps {
  view: "map" | "list";
  setView: (view: "map" | "list") => void;
}


export default function ViewToggle({ view, setView }: ViewToggleProps) {
  return (
    <div className="absolute top-5 right-5 z-50">
      <button
        onClick={() => setView(view === "map" ? "list" : "map")}
        className="p-3 bg-black/40 backdrop-blur-md rounded-full shadow-lg text-white hover:text-yellow-400 transition-transform transform hover:scale-110"
        aria-label="Toggle view"
      >
        {view === "map" ? <FaList size={20} /> : <FaMap size={20} />}
      </button>
    </div>
  );
}
