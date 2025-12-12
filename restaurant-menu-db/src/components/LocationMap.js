"use client";

import { GoogleMap, MarkerF, useLoadScript } from "@react-google-maps/api";
import { useMemo, useRef, useEffect } from "react";



export default function MapView({
  locations,
}) {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });
  const mapRef = useRef(null);
  const onLoad = (map) => {
    mapRef.current = map;
  };
  // Center = Munich example (48.07, 11.52)
  const defaultCenter = useMemo(
    () => ({ lat: 48.07, lng: 11.52 }),
    []
  );


  const getMarkerIcon = (rating) => {
  const numRating = parseFloat(rating) || 0;

  // Dynamic scale & color
  const size = 30 + (numRating - 3) * 8; // 3★=30px → 5★=46px
  let color = '#f87171'; // red by default

  if (numRating >= 4.5) color = '#22c55e'; // green
  else if (numRating >= 3.5) color = '#facc15'; // yellow
  else if (numRating >= 2.5) color = '#fb923c'; // orange

  // Custom SVG marker as Data URI (so no external files)
  const svg = `
    <svg width="${size}" height="${size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
      <circle cx="32" cy="32" r="18" fill="${color}" stroke="white" stroke-width="3"/>
      <text x="32" y="38" text-anchor="middle" font-size="20" font-weight="light" fill="white">${numRating.toFixed(1)}</text>
    </svg>
  `;
  return {
    url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`,
    scaledSize: new window.google.maps.Size(size, size),
  };
};



  // Fit map to markers when loaded
  useEffect(() => {
    if (!mapRef.current || locations.length === 0) return;

    const bounds = new window.google.maps.LatLngBounds();
    locations.forEach((loc) =>
      bounds.extend({
        lat: parseFloat(loc.latitude),
        lng: parseFloat(loc.longitude),
      })
    );

    mapRef.current.fitBounds(bounds);
  }, [locations]);


  
  if (!isLoaded)
    return <p className="text-white text-center">Loading map…</p>;

  return (
    <GoogleMap
      onLoad={onLoad}
      zoom={13}
      center={defaultCenter}
      mapContainerClassName="w-full h-full  overflow-hidden"
      options={{
        disableDefaultUI: true,
        zoomControl: true,
        gestureHandling: "greedy",
     
      }}
    >
      {locations.map((loc) => (
        <MarkerF
          key={loc.id}
          position={{
            lat: parseFloat(loc.latitude),
            lng: parseFloat(loc.longitude),
          }}
          title={loc.name || loc.category || "Restaurant"}
          icon={getMarkerIcon(loc.rating)}
        />
      ))}
    </GoogleMap>
  );
}

// Optional beautiful dark style
const darkMapStyle = [
  { elementType: "geometry", stylers: [{ color: "#1d1d1d" }] },
  { elementType: "labels.text.fill", stylers: [{ color: "#ffffff" }] },
  { elementType: "labels.text.stroke", stylers: [{ color: "#000000" }] },
];
