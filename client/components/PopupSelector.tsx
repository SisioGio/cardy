"use client";

import { useEffect, useState } from "react";

interface PopupSelectorProps {
  title: string;
  options: string[];
  selected?: string;
  onSelect: (v: string) => void;
  onClose: () => void;
}

export default function PopupSelector({
  title,
  options,
  selected,
  onSelect,
  onClose,
}: PopupSelectorProps) {
  const [search, setSearch] = useState("");

  // Filter options based on search term
  const filteredOptions = options.filter((opt) =>
    opt.toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    const onEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onEsc);
    return () => window.removeEventListener("keydown", onEsc);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 space-y-4 animate-fadeIn border border-gray-300">
        {/* Title */}
        <h2 className="text-2xl font-bold text-gray-900">{title}</h2>

        {/* Search Input */}
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-2 rounded-lg border text-gray-900 border-gray-300 outline-none focus:ring-2 focus:ring-cyan-400"
        />

        {/* Options List */}
        <div className="max-h-72 overflow-y-auto space-y-2 pr-2 scrollbar-thin scrollbar-thumb-gray-400">
          {filteredOptions.length > 0 ? (
            filteredOptions.map((opt) => (
              <button
                key={opt}
                onClick={() => onSelect(opt)}
                className={`w-full text-left px-4 py-3 rounded-lg font-medium transition
                          ${
                            selected === opt
                              ? "bg-blue-600 text-white"
                              : "bg-gray-100 text-gray-900 hover:bg-gray-200"
                          }`}
              >
                {opt || "(none)"}
              </button>
            ))
          ) : (
            <p className="text-gray-400 px-4 py-2">No results found.</p>
          )}
        </div>

        {/* Close Button */}
        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-gray-300 hover:bg-gray-400 font-medium text-gray-900 transition"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
