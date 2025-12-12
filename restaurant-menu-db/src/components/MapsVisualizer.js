import { GoogleMap, Marker, InfoWindow, useJsApiLoader } from '@react-google-maps/api';
import { useState } from 'react';

const containerStyle = { width: '100%', height: '100%',position:'relative' };
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
export default function RestaurantMap({ restaurants }) {
  const [selected, setSelected] = useState(null);
  const { isLoaded } = useJsApiLoader({
    id: process.env.REACT_APP_PROJECT_ID,
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });

  // Convert dictionary to array
  const restaurantArray = Object.values(restaurants);

  return isLoaded ? (

    <div className='absolute w-full h-screen   top-0 z-0'>

  
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={{ lat: 48.137, lng: 11.575 }} // Munich
      zoom={13}
    >
      {restaurantArray.map((r) => (
       <Marker
  key={r.rest_place_id}
  position={{
    lat: r.rest_latitude ? parseFloat(r.rest_latitude.toString().replace(',', '.')) : 0,
    lng: r.rest_longitude ? parseFloat(r.rest_longitude.toString().replace(',', '.')) : 0,
  }}
  icon={getMarkerIcon(r.rest_rating)}
  onClick={() => setSelected(r)}
/>
      ))}

      {selected && (
        <InfoWindow
          position={{ lat: parseFloat(selected.rest_latitude), lng: parseFloat(selected.rest_longitude) }}
          onCloseClick={() => setSelected(null)}
        >
          <div className="max-w-sm p-4 bg-white rounded-lg shadow-lg overflow-y-auto max-h-96">
            {/* Restaurant Info */}
            <div className="mb-3">
              <h2 className="text-lg font-bold">{selected.rest_name}</h2>
              <p className="text-sm text-gray-600">{selected.rest_city}, {selected.rest_country}</p>
              {selected.rest_photo && (
                <img src={selected.rest_photo} alt={selected.rest_name} className="w-full my-2 rounded" />
              )}
              <a
                href={selected.rest_location_link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 underline text-sm"
              >
                View on Google Maps
              </a>
            </div>

            {/* Menu */}
            <div>
              <h3 className="text-md font-semibold mb-2">Menu</h3>
              {selected.menu.map((meal) => (
                <div key={meal.item_id} className="mb-3 border-b pb-2 last:border-b-0">
                  <div className="flex justify-between items-center">
                    <h4 className="font-medium">{meal.meal_name}</h4>
                    <span className="text-sm font-semibold">{meal.meal_price}</span>
                  </div>
                  <p className="text-xs text-gray-700 my-1">{meal.meal_short_description}</p>
                  <div className="flex flex-wrap gap-1">
                    {meal.meal_is_vegan === "True" && (
                      <span className="text-xs bg-green-100 text-green-800 px-1 rounded">Vegan</span>
                    )}
                    {meal.meal_is_gluten_free === "True" && (
                      <span className="text-xs bg-yellow-100 text-yellow-800 px-1 rounded">Gluten-Free</span>
                    )}
                    {meal.meal_is_nut_free === "True" && (
                      <span className="text-xs bg-blue-100 text-blue-800 px-1 rounded">Nut-Free</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>

    </div>
  ) : (
    <div>Loading map...</div>
  );
}
