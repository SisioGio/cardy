import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronUp, SlidersHorizontal, RotateCcw } from "lucide-react";

export default function FiltersPanel({ filters, handleFilterChange, resetFilters }) {
  const [isOpen, setIsOpen] = useState(true);

  const dropdownFilters = [
    { key: "meal_cuisine_type", label: "Cuisine Type", options: ["Classic European", "Italian", "Asian", "Mexican"] },
    { key: "meal_spiciness_level", label: "Spiciness Level", options: ["mild", "medium", "hot"] },
  ];

  const checkboxFilters = [
    { key: "meal_is_gluten_free", label: "Gluten Free" },
    { key: "meal_is_vegan", label: "Vegan" },
    { key: "meal_is_nut_free", label: "Nut Free" },
    { key: "meal_is_vegetarian", label: "Vegetarian" },
    { key: "meal_is_dairy_free", label: "Dairy Free" },
    { key: "meal_is_low_carb", label: "Low Carb" },
  ];

  // Unified handler that also closes the panel after change
  const handleSelectAndClose = (key, value) => {
    handleFilterChange(key, value);
    setTimeout(() => setIsOpen(false), 250); // small delay for UX smoothness
  };

  return (
    <div className="absolute top-4 left-0 sm:left-4 z-50 w-full sm:w-80">
      {/* Neon Glow Aura */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 via-indigo-500/10 to-fuchsia-500/20 rounded-3xl -z-10 animate-pulse" />

      {/* Main Panel */}
      <div className="relative bg-slate-900/60  border border-cyan-400/40  rounded-2xl overflow-hidden">
        {/* Header */}
        <div
          onClick={() => setIsOpen(!isOpen)}
          className="flex justify-between items-center cursor-pointer bg-gradient-to-r from-cyan-500/70 via-indigo-600/70 to-fuchsia-500/70 px-5 py-3 rounded-t-2xl border-b border-cyan-300/20 hover:from-cyan-400/60 hover:to-fuchsia-400/60 transition-all"
        >
          <div className="flex items-center gap-2 text-cyan-100 drop-shadow-sm">
            <SlidersHorizontal className="w-5 h-5 animate-pulse-slow" />
            <h2 className="text-lg font-semibold tracking-widest uppercase">
              Filters
            </h2>
          </div>
          {isOpen ? (
            <ChevronUp className="w-5 h-5 text-cyan-200 transition-transform" />
          ) : (
            <ChevronDown className="w-5 h-5 text-cyan-200 transition-transform" />
          )}
        </div>

        {/* Animated Content */}
        <AnimatePresence initial={false}>
          {isOpen && (
            <motion.div
              key="filters-content"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
              className="overflow-hidden px-4 py-5 text-cyan-100"
            >
              {/* Dropdowns */}
              <div className="flex flex-col gap-3">
                {dropdownFilters.map((f) => (
                  <div key={f.key} className="relative">
                    <label className="block text-cyan-200/90 text-xs uppercase tracking-wider mb-1 font-semibold">
                      {f.label}
                    </label>
                    <select
                      onChange={(e) => handleSelectAndClose(f.key, e.target.value)}
                      value={filters[f.key] || ""}
                      className="w-full bg-slate-800/80 border border-cyan-400/50 text-cyan-100 text-sm rounded-lg px-3 py-2 focus:ring-2 focus:ring-cyan-400 focus:border-cyan-300 backdrop-blur-md transition"
                    >
                      <option value="" className="bg-slate-900 text-gray-400">
                        Select...
                      </option>
                      {f.options.map((opt) => (
                        <option
                          key={opt}
                          value={opt}
                          className="bg-slate-900 text-cyan-100"
                        >
                          {opt}
                        </option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>

              {/* Checkboxes */}
              <div className="mt-5 flex flex-col gap-2">
                <p className="text-xs uppercase tracking-widest text-cyan-300/80 font-semibold mb-1">
                  Dietary Filters
                </p>
                {checkboxFilters.map((f) => (
                  <label
                    key={f.key}
                    className="flex items-center gap-2 text-sm hover:text-cyan-200 transition"
                  >
                    <input
                      type="checkbox"
                      checked={filters[f.key] === "True"}
                      onChange={(e) =>
                        handleSelectAndClose(f.key, e.target.checked ? "True" : "False")
                      }
                      className="w-4 h-4 accent-cyan-400 bg-transparent border border-cyan-400/50 rounded-sm focus:ring-2 focus:ring-cyan-400 transition-all"
                    />
                    <span className="text-cyan-100 font-medium">{f.label}</span>
                  </label>
                ))}
              </div>

              {/* Reset Button */}
              <div className="flex justify-center gap-3 mt-6 flex-wrap">
                <motion.button
                  whileHover={{ scale: 1.05, boxShadow: "0 0 25px rgba(255,255,255,0.25)" }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    resetFilters();
                    setTimeout(() => setIsOpen(false), 250);
                  }}
                  className="flex items-center justify-center gap-2 bg-gradient-to-r from-pink-600/40 to-fuchsia-600/40 hover:from-pink-500/60 hover:to-fuchsia-500/60 text-white font-semibold px-6 py-2.5 rounded-lg border border-pink-400/40 shadow-inner transition-all w-full sm:w-auto"
                >
                  <RotateCcw className="h-4" />
                  Reset
                </motion.button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
