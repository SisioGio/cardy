"use client";

import { useState } from "react";

export default function LocationList({ locations }) {
  const [expandedLocations, setExpandedLocations] = useState(new Set());
  const [expandedMenuItems, setExpandedMenuItems] = useState(new Set());

  const toggleLocation = (id: string | number) => {
    setExpandedLocations((prev) => {
      const newSet = new Set(prev);
      newSet.has(id) ? newSet.delete(id) : newSet.add(id);
      return newSet;
    });
  };

  const toggleMenuItem = (id: string | number) => {
    setExpandedMenuItems((prev) => {
      const newSet = new Set(prev);
      newSet.has(id) ? newSet.delete(id) : newSet.add(id);
      return newSet;
    });
  };

  return (
    <div className="space-y-6 p-2">
      {locations.map((loc) => (
        <div
          key={loc.id}
          className="bg-white shadow-md rounded-xl p-5 border border-gray-200 hover:shadow-lg transition-shadow duration-200"
        >
          {/* --- Header --- */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="flex items-center gap-4">
              {loc.photo && (
                <img
                  src={loc.photo}
                  alt={loc.name}
                  className="h-20 w-20 object-cover rounded-lg shadow-sm"
                />
              )}
              <div className="flex flex-col">
                <h2 className="text-xl font-semibold text-gray-800">{loc.name.split("-")[0]}</h2>
                <div className="flex flex-wrap gap-2 mt-1 text-sm text-gray-600">
                  {loc.type && <span>{loc.type}</span>}
                  {loc.price_range && <span>Price: {loc.price_range}/5</span>}
                  {loc.rating && <span>⭐ {loc.rating}</span>}
                </div>

                {/* Services Preview */}
                {Array.isArray(loc.services) && loc.services.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2 text-sm">
                    {(() => {
                      const trueServices = loc.services.filter((s) => s.value === true);
                      const maxPreview = 3;
                      const preview = trueServices.slice(0, maxPreview);
                      return (
                        <>
                          {preview.map((s, idx) => (
                            <span
                              key={idx}
                              className="bg-gray-200 text-gray-700 px-2 py-0.5 rounded-full"
                            >
                              {s.key}
                            </span>
                          ))}
                          {trueServices.length > maxPreview && (
                            <span className="bg-gray-200 text-gray-700 px-2 py-0.5 rounded-full">
                              +{trueServices.length - maxPreview} more
                            </span>
                          )}
                        </>
                      );
                    })()}
                  </div>
                )}
              </div>
            </div>

            <button
              onClick={() => toggleLocation(loc.id)}
              className="text-gray-500 hover:text-gray-700 text-sm font-medium transition"
            >
              {expandedLocations.has(loc.id) ? "Hide Details" : "Show Details"}
            </button>
          </div>

          {/* --- Expanded Details --- */}
          {expandedLocations.has(loc.id) && (
            <div className="mt-4 space-y-4">
              {/* Links */}
              <div className="flex flex-wrap gap-4">
                {loc.booking_link && (
                  <a
                    href={loc.booking_link}
                    rel="noreferrer"
                    target="_blank"
                    className="text-blue-600 underline text-sm hover:text-blue-800 transition"
                  >
                    Booking
                  </a>
                )}
                {loc.order_link && (
                  <a
                    href={loc.order_link}
                    rel="noreferrer"
                    target="_blank"
                    className="text-blue-600 underline text-sm hover:text-blue-800 transition"
                  >
                    Order
                  </a>
                )}
                {loc.reservation_link && (
                  <a
                    href={loc.reservation_link}
                    rel="noreferrer"
                    target="_blank"
                    className="text-blue-600 underline text-sm hover:text-blue-800 transition"
                  >
                    Reserve
                  </a>
                )}
              </div>

              {/* Working Hours */}
              {Array.isArray(loc.working_hours) && loc.working_hours.length > 0 && (
                <div className="text-gray-600 text-sm">
                  <strong>Working Hours:</strong>
                  <ul className="list-disc ml-5 mt-1">
                    {loc.working_hours.map((wh, idx) => (
                      <li key={idx}>
                        {wh.day}: {wh.from} - {wh.to || "Open"}{" "}
                        {wh.is_closed ? "(Closed)" : ""}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Menu Items */}
              {Array.isArray(loc.menu_items) && loc.menu_items.length > 0 && (
                <div className="space-y-3">
                  {loc.menu_items.map((item) => (
                    <div
                      key={item.id}
                      className="border border-gray-200 p-3 rounded-lg hover:border-gray-400 transition-colors"
                    >
                      <div className="flex justify-between items-center">
                        <h3 className="font-medium text-gray-800">{item.name}</h3>
                        {item.price && (
                          <span className="text-gray-700 font-medium">{item.price}€</span>
                        )}
                        <button
                          onClick={() => toggleMenuItem(item.id)}
                          className="text-gray-500 hover:text-gray-700 text-sm ml-2 transition"
                        >
                          {expandedMenuItems.has(item.id) ? "Hide" : "Show"}
                        </button>
                      </div>

                      {expandedMenuItems.has(item.id) && item.full_description && (
                        <p className="text-gray-600 text-sm mt-2">{item.full_description}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      ))}


      
    </div>
  );
}
