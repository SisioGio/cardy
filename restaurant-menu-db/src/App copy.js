import React, { useEffect, useState } from 'react';
import './App.css';
import MenuItems from './components/FilterPanel';
import RestaurantMap from './components/MapsVisualizer';
import LoadingOverlay from './components/LoadingScreen';
import LocationList from './components/LocationsList';

const initialStateFilters = {
  // Meal properties
  meal_is_gluten_free: '',
  meal_is_vegan: '',
  meal_is_nut_free: '',
  meal_is_low_carb: '',
  meal_is_dairy_free: '',
  meal_is_vegetarian: '',
        
  meal_preparation_method: '',
  meal_price: '',
  meal_cuisine_type: '',
  meal_name: '',
  meal_meal_category: '',

  meal_spiciness_level: '',
  rest_rating: '',
  rest_working_hours: '',
  rest_type: '',
  rest_postal_code: '',
  rest_subtypes: '',
  rest_category: '',
  rest_borough: '',
  rest_name: '',
  rest_street: '',
  rest_country: '',
  rest_full_address: '',
  rest_city: ''
}



function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const [filters, setFilters] = useState({

  meal_is_gluten_free: '',
  meal_is_vegan: '',
  meal_is_nut_free: '',
  meal_is_low_carb: '',
  meal_is_dairy_free: '',
  meal_is_vegetarian: '',
  
  meal_preparation_method: '',
  meal_price: '',
  meal_cuisine_type: '',
  meal_name: '',
  meal_meal_category: '',

  meal_spiciness_level: '',


  rest_rating: '',
  rest_working_hours: '',
  rest_type: '',
  rest_postal_code: '',
  rest_subtypes: '',
  rest_category: '',
  rest_borough: '',
  rest_name: '',
  rest_street: '',
  rest_country: '',
  rest_full_address: '',
  rest_city: ''
    });

  
  const fetchData = async () => {
    setLoading(true);
    try {

      const query = Object.entries(filters)
            .filter(([_, v]) => v !== '' && v !== null && v !== undefined )
            .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
            .join('&');

      const res = await fetch(`https://4gzaqe6jpa.execute-api.eu-central-1.amazonaws.com/dev/public?${query}`);
      const data = await res.json();
      setItems(data.rows || []);
    } catch (err) {
      console.error('Error fetching data', err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);


  useEffect(() => {
    fetchData();
  }, [filters]);


  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value });
  };

  const resetFilters = () => {
    setFilters({...initialStateFilters});
    
  };

  return (
     <div className="relative h-screen w-full flex flex-col">


      <LocationList locations={items}/>
      
      {/* <MenuItems items={items} setItems={setItems} handleFilterChange={handleFilterChange} resetFilters={resetFilters} loading={loading} fetchData={fetchData} filters={filters}/>
       <LoadingOverlay loading={loading}/>
     <RestaurantMap restaurants={items}/> */}
     
     </div>
  );
}

export default App;
