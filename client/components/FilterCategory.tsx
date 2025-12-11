"use client";
import Select from "react-dropdown-select";
import { FilterDescriptor, FilterOptions } from "@/types/location";
import PopupSelector from "./PopupSelector";
import { useState } from "react";

interface Props {
  key: string;
  filters: Record<string, string>;
  filter:FilterDescriptor,
  filterDescription: Record<string, string>;
  filterId:string,
  handleChange: (key: string, value: any) => void;
  options: Record<string, FilterOptions>;
}

export default function FilterCategory({
  key,
  filter,
  filters,
  filterId,
  filterDescription,
  handleChange,
  options,
}: Props) {
  const [open, setOpen] = useState(true);
    const [popupOpen, setPopupOpen] = useState(false);
  const toggle = () => setOpen((s) => !s);

  const capitalize = (str: string) =>
    str ? str.charAt(0).toUpperCase() + str.slice(1) : "";

  const renderInput = (key: string, filter: FilterDescriptor) => {
    const opt = options[key];
    console.log(key,filter)
    // STRING field with dropdown options
    if (filter.type === "string") {
      if (opt?.options?.length > 0) {
        return (
      <>
        {/* Field display */}
        <button
          onClick={() => setPopupOpen(true)}
          className="bg-white/20 text-white px-3 py-2 rounded-lg text-left w-full 
                     hover:bg-white/30 transition"
        >
          {filters[key] || `Select ${filter.label}`}
        </button>

        {/* Popup modal */}
        {popupOpen && (
          <PopupSelector
            title={filter.label}
            selected={filters[key]}
            options={opt.options}
            onSelect={(value) => {
              handleChange(key, value);
              setPopupOpen(false);
            }}
            onClose={() => setPopupOpen(false)}
          />
        )}
      </>
    );
      }

      // STRING field without options
      return (
        <input
          type="text"
          placeholder={filter.label}
          className="bg-white/20 text-white p-2 rounded-lg outline-none focus:ring-2 ring-cyan-400"
          value={filters[key] || ""}
          onChange={(e) => handleChange(key, e.target.value)}
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
              checked={filters[key] === "true"}
              onChange={(e) =>
                handleChange(key, e.target.checked ? "true" : "false")
              }
              className="sr-only peer"
            />
            <div className="w-11 h-6 bg-white/20 rounded-full peer peer-checked:bg-green-500 transition-colors"></div>
            <div className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full peer-checked:translate-x-5 transition-transform"></div>
          </div>
          <span className="text-sm text-gray-200">{filter.label}</span>
        </label>
      );
    }

    // NUMBER RANGE
    if (filter.type === "number") {
      return (
        <div className="grid grid-cols-2 gap-2">
          <input
            type="number"
            placeholder="Min"
            className="bg-white/20 text-white p-2 rounded-lg outline-none focus:ring-2 ring-cyan-400"
            value={filters[key + "_min"] || ""}
            onChange={(e) => handleChange(key + "_min", e.target.value)}
          />
          <input
            type="number"
            placeholder="Max"
            className="bg-white/20 text-white p-2 rounded-lg outline-none focus:ring-2 ring-cyan-400"
            value={filters[key + "_max"] || ""}
            onChange={(e) => handleChange(key + "_max", e.target.value)}
          />
        </div>
      );
    }

    // FALLBACK
    return (
      <input
        type="text"
        placeholder={filter.label}
        className="bg-white/20 text-white p-2 rounded-lg outline-none focus:ring-2 ring-cyan-400"
        value={filters[key] || ""}
        onChange={(e) => handleChange(key, e.target.value)}
      />
    );
  };


  
  return (
    <div className="bg-white/5 rounded-lg border border-white/10 overflow-hidden shadow-sm">
  
      

     
        <div className="p-4 pt-1 space-y-4 max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-white/20">
    
              <div key={key} className="flex flex-col gap-1">
                {filter.type !== "bool" && (
                  <label className="text-sm text-gray-300">
                    {filter.label}
                  </label>
                )}

                {renderInput(filterId, filter)}
              </div>
            
        </div>
     
    </div>
  );
}
