import React, { useEffect, useState } from 'react';
import FilterBar from '../components/FilterBar';
import MapView from '../components/LocationMap';
import ViewToggle from '../components/ViewToggle.tsx';
import LocationList from '../components/LocationsList.tsx';
import PaginationControls from '../components/PaginationControls.js';


function Explorer() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters,setFilters] = useState({})
  const [options,setOptions] = useState({})
  const [view, setView] = useState("list");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const [pageSize,setPageSize] = useState(10)

  // ----------------------------------------
  // Build query string
  // ----------------------------------------
  const buildQuery = () => {
    const params = new URLSearchParams({
      lat: "48.07",
      lng: "11.52",
      range: "10",
    });
    if(view==='list'){
      params.append('paginate',true)
      params.append('page',page)
      params.append('page_size',pageSize)

    } else{
      params.append('paginate',false)
      params.delete('page')
      params.delete("page_size")
    }
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== "") params.append(key, value);
    });

    return params.toString();
  };




  const fetchAllData = async () => {
    setLoading(true);
    try {

      const query = buildQuery();
      const res = await fetch(`https://4gzaqe6jpa.execute-api.eu-central-1.amazonaws.com/dev/public?${query}`);
      const data = await res.json();
      setItems(data.rows || []);
      setOptions(data.options || {});
      setTotalPages(data.total_pages);
    } catch (err) {
      console.error('Error fetching data', err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  useEffect(() => {
    fetchAllData();
  }, [filters]);
 useEffect(() => {
    fetchAllData();
  }, [view]);
 useEffect(() => {
    fetchAllData();
  }, [page]);
 // ----------------------------------------
  // Perform search after clicking "Search"
  // ----------------------------------------
  const handleSearch = () => {
    fetchAllData();
  };

  // ----------------------------------------
  // Reset filters
  // ----------------------------------------
  const resetFilters = () => {
    setFilters({});
   
  };
    

  return (
    <div className="flex w-full h-[calc(100vh-5rem)]   overflow-hidden">
  {/* -------- SIDEBAR -------- */}
  <aside className="
      w-full xl:w-80
      bg-gradient-to-b from-purple-900/40 via-pink-900/30 to-red-900/30
      backdrop-blur-md p-5 border-r border-white/10
      shadow-2xl flex-shrink-0
      overflow-y-auto
    "
  >
    <h3 className="text-3xl font-extrabold text-white tracking-wide mb-3">
      Filters
    </h3>

    <FilterBar filters={filters} setFilters={setFilters} options={options} />

    <div className="flex gap-3 mt-4">
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
  </aside>

  {/* -------- MAIN CONTENT -------- */}
  <main className="flex flex-col flex-grow overflow-hidden">

    {/* Toggle Buttons */}
    <div className="p-3 border-b border-gray-200 bg-white/80 backdrop-blur-md">
      <ViewToggle view={view} setView={setView} />
    </div>

    {/* Active Filters Row */}
    <div className="flex flex-wrap gap-2 p-3 bg-white border-b border-gray-200">
      {Object.entries(filters)
        .filter(([k, v]) => v && v !== "" && v !== "false")
        .map(([key, value]) => (
          <div
            key={key}
            className="flex items-center gap-1 bg-gray-900 text-white px-3 py-1 rounded-full shadow hover:scale-105 transition"
          >
            <span className="capitalize text-sm">
              {key.replace(/_/g, " ")}: {value}
            </span>
            <button
              onClick={() => setFilters(prev => ({ ...prev, [key]: "" }))}
              className="w-5 h-5 flex items-center justify-center bg-white/20 hover:bg-white/40 rounded-full text-xs font-bold text-white"
            >
              ×
            </button>
          </div>
        ))}
    </div>

    {/* -------- VIEWS -------- */}
    {view === "map" ? (
      <div className="flex-grow overflow-hidden">
        <MapView locations={items} />
      </div>
    ) : (
      <div className="flex flex-col flex-grow overflow-hidden">

        {/* Scrollable List Area */}
        <div className="flex-grow overflow-y-auto p-4">
          <LocationList locations={items} />
        </div>

        {/* Pagination Stays Visible */}
        <div className="p-3 border-t bg-white">
          <PaginationControls
            page={page}
            setPage={setPage}
            totalPages={totalPages}
          />
        </div>

      </div>
    )}
  </main>
</div>

  );
}

export default Explorer;