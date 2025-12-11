"use client";

import { useState } from "react";
import { restaurantFilters } from "@/filters/restaurantFilters";
import { FilterOptions } from "@/types/location";
import FilterCategory from "./FilterCategory";

type Filters = Record<string, string>;

interface FilterBarProps {
  filters: Filters;
  setFilters: (f: Record<string, string>) => void;
  options: Record<string, FilterOptions>;
}

export default function FilterBar({ filters, setFilters, options }: FilterBarProps) {
  const [open, setOpen] = useState<Record<string, boolean>>({});

  const toggleCategory = (cat: string) => {
    setOpen(prev => ({ ...prev, [cat]: !prev[cat] }));
  };

  const handleChange = (key: string, value: string) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
    }));
  };


  if (!options){
    return (
        <small>Loading...</small>
    )
  }

  return (
    <div className="bg-white/10 backdrop-blur-md p-4 rounded-xl shadow-xl mb-4 space-y-4 border border-white/5">
      <h3 className="text-xl font-semibold text-white tracking-wide mb-1">Filters</h3>

      <div className="space-y-3">
        {Object.entries(restaurantFilters).map(([category, catFilters]) => (
          <div
            key={category}
            className="bg-white/5 rounded-lg overflow-hidden border border-white/10"
          >
            {/* -------------------- CATEGORY HEADER -------------------- */}
            <button
              className="w-full flex justify-between items-center px-4 py-3 text-left text-white/90 hover:bg-white/10 transition-colors"
              onClick={() => toggleCategory(category)}
            >
              <span className="font-medium text-base capitalize">{category}</span>

              <span className="text-white/60 text-sm">
                {open[category] ? "▲" : "▼"}
              </span>
            </button>

            {/* -------------------- CATEGORY BODY -------------------- */}
            {open[category] && (
              <div className="p-3 pt-0 max-h-96 overflow-y-auto space-y-3 scrollbar-thin scrollbar-thumb-white/20">
                {Object.entries(catFilters).map(([key, filter]) => (

                  
                  <FilterCategory
                    key={key}
                    filterId={key}
                    filter={filter}
                    filterDescription={filter}
                    filters={filters}
                    handleChange={handleChange}
                    options={options}
                  />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
