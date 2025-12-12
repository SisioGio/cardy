"use client";

import { useState } from "react";
import { restaurantFilters } from "../static/RestaurantFilters";
import FilterCategory from "./FilterCategory";

export default function FilterBar({ filters, setFilters, options }) {
  const [open, setOpen] = useState({});

  const toggleCategory = (cat) => {
    setOpen((prev) => ({ ...prev, [cat]: !prev[cat] }));
  };

  const handleChange = (key, value) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  if (!options) return <small className="text-gray-400">Loading filters...</small>;

  return (
 

      <div className="space-y-4">
        {Object.entries(restaurantFilters).map(([category, catFilters]) => (
          <div
            key={category}
            className="bg-gradient-to-r from-purple-700/30 via-pink-600/20 to-red-500/20 rounded-2xl border border-white/20 overflow-hidden shadow-md hover:shadow-xl transition-shadow"
          >
            {/* Category Header */}
            <button
              className="w-full flex justify-between items-center px-6 py-4 text-left text-white font-semibold text-lg hover:bg-white/10 transition-colors"
              onClick={() => toggleCategory(category)}
            >
              <span className="capitalize">{category}</span>
              <span
                className={`text-white/70 text-sm transition-transform duration-300 ${
                  open[category] ? "rotate-180" : ""
                }`}
              >
                ▼
              </span>
            </button>

            {/* Category Body */}
            <div
              className={`overflow-y-auto transition-all duration-300 ${
                open[category] ? "max-h-96 p-5" : "max-h-0 p-0"
              }`}
            >
              <div className="space-y-4">
                {Object.entries(catFilters).map(([key, filter]) => (
                  <FilterCategory
                    key={key}
                    filterId={key}
                    filter={filter}
                    filters={filters}
                    handleChange={handleChange}
                    options={options}
                  />
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
 
  );
}
