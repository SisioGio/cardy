"use client";

import { useEffect, useState } from "react";
import { Location, WorkingHour } from "@/types/location";
import {Service} from '@/types/location'
import {MenuItem} from '@/types/location'



export default function LocationList({locations}:{locations: Location[]}) {
  
  const [expandedLocations, setExpandedLocations] = useState<Set<string>>(new Set());
  const [expandedMenuItems, setExpandedMenuItems] = useState<Set<string>>(new Set());

 

  const toggleLocation = (id: string) => {
    setExpandedLocations((prev) => {
      const newSet = new Set(prev);
      newSet.has(id) ? newSet.delete(id) : newSet.add(id);
      return newSet;
    });
  };

  const toggleMenuItem = (id: string) => {
    setExpandedMenuItems((prev) => {
      const newSet = new Set(prev);
      newSet.has(id) ? newSet.delete(id) : newSet.add(id);
      return newSet;
    });
  };



  return (
    <div className="space-y-6">
      {locations.map((loc) => (
        <div
          key={loc.id}
          className="bg-black/60 backdrop-blur-md rounded-xl shadow-xl p-5 hover:shadow-cyan-500/40 transition-shadow duration-300"
        >
          {/* --- Header --- */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="flex items-center gap-4">
              {loc.photo && (
                <img
                  src={loc.photo}
                  alt={loc.name}
                  className="h-20 w-20 object-cover rounded-lg shadow-md"
                />
              )}
              <div>
                <h2 className="text-2xl font-bold text-cyan-400">{loc.name.split("-")[0]}</h2>
                <div className="flex flex-wrap gap-2 mt-1">
                  {loc.type && <span className="text-gray-300 text-sm">{loc.type}</span>}
                  {/* {loc.category && <span className="text-gray-300 text-sm">{loc.category}</span>} */}
                  {loc.price_range && <span className="text-yellow-300 text-sm">{loc.price_range}/5</span>}
                  {loc.rating && <span className="text-green-400 text-sm">⭐ {loc.rating}</span>}
                </div>
                {/* --- Services Preview --- */}
{Array.isArray(loc.services) && loc.services.length > 0 && (
  <div className="flex flex-wrap gap-2 mt-2">
    {(() => {
      // Filter only "true" services
      const trueServices = loc.services.filter((s: Service) => s.value === true);
      const maxPreview = 3;
      const preview = trueServices.slice(0, maxPreview);
      return (
        <>
          {preview.map((s: Service, idx: number) => (
            <span
              key={idx}
              className="bg-purple-700 text-white text-xs px-2 py-0.5 rounded-full"
            >
              {s.key}
            </span>
          ))}
          {trueServices.length > maxPreview && (
            <span className="bg-gray-600 text-white text-xs px-2 py-0.5 rounded-full">
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
              className="text-purple-400 hover:text-purple-200 text-sm font-medium"
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
                    target="_blank"
                    className="text-cyan-300 underline text-sm"
                  >
                    Booking
                  </a>
                )}
                {loc.order_link && (
                  <a
                    href={loc.order_link}
                    target="_blank"
                    className="text-cyan-300 underline text-sm"
                  >
                    Order
                  </a>
                )}
                {loc.reservation_link && (
                  <a
                    href={loc.reservation_link}
                    target="_blank"
                    className="text-cyan-300 underline text-sm"
                  >
                    Reserve
                  </a>
                )}
              </div>

              {/* Services */}
              {Array.isArray(loc.services) && loc.services.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {loc.services.map((s: Service, idx: number) => (
                    <span
                      key={idx}
                      className="bg-purple-700 text-white text-xs px-2 py-0.5 rounded-full"
                    >
                      {s.key}: {s.value?.toString()}
                    </span>
                  ))}
                </div>
              )}

              {/* Working Hours */}
              {Array.isArray(loc.working_hours) && loc.working_hours.length > 0 && (
                <div className="text-gray-300 text-sm">
                  <strong>Working Hours:</strong>
                  <ul>
                    {loc.working_hours.map((wh: WorkingHour, idx: number) => (
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
                  {loc.menu_items.map((item: MenuItem) => (
                    <div
                      key={item.id}
                      className="border border-gray-700 p-3 rounded-lg hover:border-cyan-400 transition-colors"
                    >
                      <div className="flex justify-between items-center">
                        <h3 className="font-semibold text-white">{item.name}</h3>
                        {item.price && <span className="text-cyan-300 font-medium">{item.price}€</span>}
                        <button
                          onClick={() => toggleMenuItem(item.id)}
                          className="text-sm text-purple-400 hover:text-purple-200 ml-2"
                        >
                          {expandedMenuItems.has(item.id) ? "Hide" : "Show"}
                        </button>
                      </div>

                      {expandedMenuItems.has(item.id) && (
                        <div className="mt-2 space-y-1">
                          {/* Full description */}
                          {item.full_description && (
                            <p className="text-gray-300 text-sm">{item.full_description}</p>
                          )}

                          {/* Pills for booleans or strings */}
                          <div className="flex flex-wrap gap-2 mt-2">
                            {Object.entries(item).map(([key, val]) => {
                              if (!val) return null;
                              if (typeof val === "boolean" && val)
                                return (
                                  <span
                                    key={key}
                                    className="bg-green-700 text-white text-xs px-2 py-0.5 rounded-full"
                                  >
                                    {key.replace(/_/g, " ")}
                                  </span>
                                );
                              if (typeof val === "string" && key !== "name" && key !== "full_description")
                                return (
                                  <span
                                    key={key}
                                    className="bg-purple-700 text-white text-xs px-2 py-0.5 rounded-full"
                                  >
                                    {val}
                                  </span>
                                );
                              return null;
                            })}
                          </div>
                        </div>
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
