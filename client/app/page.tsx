"use client";

import { useState, useEffect } from "react";
import LocationList from "@/components/LocationList";
import LocationMap from "@/components/LocationMap";
import ViewToggle from "@/components/ViewToggle";
import FilterBar from "@/components/FilterBar";
import { FilterOptions } from "@/types/location";

export default function HomePage() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<"list" | "map">("map");
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [options, setOptions] = useState<Record<string, FilterOptions>>({});

  // ----------------------------------------
  // Build query string
  // ----------------------------------------
  const buildQuery = () => {
    const params = new URLSearchParams({
      lat: "48.07",
      lng: "11.52",
      range: "10",
    });

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== "") params.append(key, value);
    });

    return params.toString();
  };

  // ----------------------------------------
  // Fetch locations
  // ----------------------------------------
  const fetchResults = async () => {
    try {
      setLoading(true);

      const query = buildQuery();
      const res = await fetch(`http://127.0.0.1:5000/locations?${query}`);

      const data = await res.json();

      setLocations(data.rows || []);
      setOptions(data.options || {});

    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  // ----------------------------------------
  // Perform search after clicking "Search"
  // ----------------------------------------
  const handleSearch = () => {
    fetchResults();
  };

  // ----------------------------------------
  // Reset filters
  // ----------------------------------------
  const resetFilters = () => {
    setFilters({});
    fetchResults();
  };

  // ----------------------------------------
  // Initial fetch
  // ----------------------------------------
  useEffect(() => {
    fetchResults();
  }, []);

  // ----------------------------------------
  // UI
  // ----------------------------------------
  if (loading) {
    return (
      <div className="flex justify-center items-center h-[80vh] text-gray-300 text-xl">
        Loading…
      </div>
    );
  }

  return (
    <div className="flex w-full h-full grow gap-4 p-4 overflow-hidden">

      {/* ----------------------------------------
          Sidebar
      ---------------------------------------- */}
      <aside className="w-80 xl:w-96 flex flex-col gap-4 overflow-y-auto pr-2">

        <h1 className="text-2xl font-semibold mb-1 tracking-wide text-white/90">
          Advanced Restaurant Search
        </h1>

        <FilterBar
          filters={filters}
          setFilters={setFilters}
          options={options}
        />

        <div className="flex gap-3 mt-2">
          <button
            onClick={handleSearch}
            className="flex-1 bg-green-500 hover:bg-green-600 transition-colors py-2 rounded-lg font-medium shadow-md"
          >
            Search
          </button>

          <button
            onClick={resetFilters}
            className="flex-1 bg-red-500 hover:bg-red-600 transition-colors py-2 rounded-lg font-medium shadow-md"
          >
            Reset
          </button>
        </div>

        <ViewToggle view={view} setView={setView} />
      </aside>

      {/* ----------------------------------------
          Main content
      ---------------------------------------- */}
      <section className="flex-1 rounded-xl overflow-hidden shadow-2xl border border-white/5 bg-black/10 backdrop-blur-sm">
        {view === "list" ? (
          <LocationList locations={locations} />
        ) : (
          <LocationMap locations={locations} />
        )}
      </section>

    </div>
  );
}
