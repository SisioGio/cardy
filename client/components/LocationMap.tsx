"use client";

import { GoogleMap, MarkerF, useLoadScript } from "@react-google-maps/api";
import { useMemo, useRef, useEffect } from "react";

type Location = {
  id: string;
  latitude: string;
  longitude: string;
  name?: string;
  category?: string;
};

export default function MapView({
  locations,
}: {
  locations: Location[];
}) {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_KEY!,
  });

  const mapRef = useRef<google.maps.Map | null>(null);

  const onLoad = (map: google.maps.Map) => {
    mapRef.current = map;
  };

  // Center = Munich example (48.07, 11.52)
  const defaultCenter = useMemo(
    () => ({ lat: 48.07, lng: 11.52 }),
    []
  );

  // Fit map to markers when loaded
  useEffect(() => {
    if (!mapRef.current || locations.length === 0) return;

    const bounds = new google.maps.LatLngBounds();
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
      mapContainerClassName="w-full h-full rounded-xl overflow-hidden"
      options={{
        disableDefaultUI: true,
        zoomControl: true,
        gestureHandling: "greedy",
        styles: darkMapStyle, // Optional dark theme
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
