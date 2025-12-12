import React, { useEffect, useState } from "react";
import { FaUtensils, FaStar, FaDollarSign, FaAllergies, FaClipboardList, FaMapMarkerAlt, FaSearch, FaFilter } from "react-icons/fa";

const HomePage = () => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => setLoaded(true), 100);
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-tr from-gray-50 to-white flex flex-col">
      <main className={`flex-grow max-w-7xl mx-auto px-6 pb-16 transition-opacity duration-700 ${loaded ? "opacity-100" : "opacity-0"}`}>

        {/* Hero Section */}
        <section className="flex flex-col-reverse md:flex-row items-center gap-12 md:gap-24 my-16">
          <div className="flex-1 text-center md:text-left">
            <h1 className="text-5xl font-extrabold text-gray-900 mb-6 leading-tight">
              Discover the <span className="text-red-600">Best Restaurants</span> Around You
            </h1>
            <p className="text-lg text-gray-700 mb-8 max-w-xl mx-auto md:mx-0">
              Explore menus, services, pricing, dietary info, and more. Find your perfect spot quickly and confidently.
            </p>
            <a
              href="/restaurants"
              className="inline-flex items-center bg-red-600 hover:bg-red-700 text-white font-semibold px-8 py-4 rounded-full shadow-lg transition"
            >
              Explore Now <FaUtensils className="ml-3" size={24} />
            </a>
          </div>

          <div className="flex-1">
            <img
              src="/restaurant-dashboard.png"
              alt="Restaurant discovery dashboard"
              className="rounded-xl mx-auto shadow-lg"
              loading="lazy"
            />
          </div>
        </section>

       

        {/* Features Section */}
        <section className="mt-20 max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
          <FeatureCard
            icon={<FaClipboardList className="text-red-600 mx-auto mb-4" size={48} />}
            title="Complete Details"
            description="Menus, services, pricing, dietary info, and nutritional facts all in one place, updated daily."
          />
          <FeatureCard
            icon={<FaStar className="text-red-600 mx-auto mb-4" size={48} />}
            title="Ratings & Reviews"
            description="See what other diners are saying and filter by top-rated restaurants, cuisine, and service."
          />
          <FeatureCard
            icon={<FaMapMarkerAlt className="text-red-600 mx-auto mb-4" size={48} />}
            title="Nearby Restaurants"
            description="Discover restaurants around your location with interactive maps and distance-based search."
          />
        </section>

        {/* Benefits Section */}
        <section className="mt-28 bg-red-600 text-white rounded-2xl p-12 max-w-6xl mx-auto shadow-lg">
          <h2 className="text-3xl font-bold mb-8 text-center">Why Choose Restaurant Explorer?</h2>
          <ul className="space-y-6 max-w-4xl mx-auto text-lg">
            <li className="flex items-center gap-4">
              <FaDollarSign size={28} className="text-green-300" />
              <span>Compare prices and services across multiple restaurants easily</span>
            </li>
            <li className="flex items-center gap-4">
              <FaAllergies size={28} className="text-green-300" />
              <span>Filter for allergens, dietary preferences, and health requirements</span>
            </li>
            <li className="flex items-center gap-4">
              <FaClipboardList size={28} className="text-green-300" />
              <span>Access complete menu information with calories, ingredients, and special notes</span>
            </li>
            <li className="flex items-center gap-4">
              <FaUtensils size={28} className="text-green-300" />
              <span>Discover hidden gems and local favorites around your area</span>
            </li>
          </ul>
        </section>

        {/* Call-to-action Section */}
        <section className="mt-20 text-center">
          <h2 className="text-3xl font-bold mb-6 text-gray-900">Start Exploring Today</h2>
          <a href="/restaurants" className="inline-flex items-center bg-red-600 hover:bg-red-700 text-white font-semibold px-10 py-4 rounded-full shadow-lg transition">
            Browse Restaurants <FaMapMarkerAlt className="ml-3" size={24} />
          </a>
        </section>
      </main>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }) => (
  <div className="bg-white rounded-xl shadow-md p-6 flex flex-col items-center">
    {icon}
    <h3 className="font-semibold text-xl mb-3">{title}</h3>
    <p className="text-gray-600 text-center">{description}</p>
  </div>
);

export default HomePage;
