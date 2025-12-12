"use client";

import { useState } from "react";
import PopupSelector from "./PopupSelector";

export default function FilterCategory({ filter, filters, filterId, handleChange, options }) {
  const [popupOpen, setPopupOpen] = useState(false);

  const renderInput = () => {
    const opt = options[filterId];

    // STRING TYPE
    if (filter.type === "string") {
      if (opt?.options?.length) {
        return (
          <>
            <button
              onClick={() => setPopupOpen(true)}
              className="w-full text-left px-4 py-3 rounded-xl bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 text-white font-medium hover:from-pink-400 hover:via-purple-400 hover:to-indigo-400 transition-all shadow-lg"
            >
              {filters[filterId] || `Select ${filter.label}`}
            </button>
            {popupOpen && (
              <PopupSelector
                title={filter.label}
                options={opt.options}
                selected={filters[filterId]}
                onSelect={(value) => {
                  handleChange(filterId, value);
                  setPopupOpen(false);
                }}
                onClose={() => setPopupOpen(false)}
              />
            )}
          </>
        );
      }

      return (
        <input
          type="text"
          placeholder={filter.label}
          value={filters[filterId] || ""}
          onChange={(e) => handleChange(filterId, e.target.value)}
          className="w-full p-3 rounded-xl bg-black/40 text-white placeholder-gray-300 border border-purple-400 focus:outline-none focus:ring-2 focus:ring-pink-400 shadow-inner transition"
        />
      );
    }

    // BOOLEAN SWITCH
    if (filter.type === "bool") {
      return (
        <label className="flex items-center gap-3 cursor-pointer select-none">
          <div className="relative inline-flex items-center">
            <input
              type="checkbox"
              checked={filters[filterId] === "true"}
              onChange={(e) => handleChange(filterId, e.target.checked ? "true" : "false")}
              className="sr-only peer"
            />
            <div className="w-12 h-6 bg-purple-700/30 rounded-full peer-checked:bg-pink-500 transition-colors"></div>
            <div className="absolute left-1 top-1 w-5 h-5 bg-white rounded-full peer-checked:translate-x-6 transition-transform shadow-md"></div>
          </div>
          <span className="text-white font-medium">{filter.label}</span>
        </label>
      );
    }

    // NUMBER RANGE
    if (filter.type === "number") {
      return (
        <div className="flex flex-col">
          <span className="text-white font-medium">{filter.label}</span>
          <div className="grid grid-cols-2 gap-3">
          <input
            type="number"
            placeholder="Min"
            value={filters[filterId + "_min"] || ""}
            onChange={(e) => handleChange(filterId + "_min", e.target.value)}
            className="p-2 rounded-xl bg-black/40 text-white placeholder-gray-300 border border-purple-400 focus:outline-none focus:ring-2 focus:ring-pink-400 shadow-inner transition"
          />
          <input
            type="number"
            placeholder="Max"
            value={filters[filterId + "_max"] || ""}
            onChange={(e) => handleChange(filterId + "_max", e.target.value)}
            className="p-2 rounded-xl bg-black/40 text-white placeholder-gray-300 border border-purple-400 focus:outline-none focus:ring-2 focus:ring-pink-400 shadow-inner transition"
          />
        </div>
             </div>
      );
    }

    return null;
  };

  return <div>{renderInput()}</div>;
}
