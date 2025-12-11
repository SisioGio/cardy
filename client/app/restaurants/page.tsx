// app/restaurants/page.tsx
import LocationList from "@/components/LocationList";

export default function RestaurantsPage() {
  return (
    <div className="pt-20 p-4  max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold glow text-white mb-6">
        Nearby Restaurants
      </h1>
      <LocationList />
    </div>
  );
}
