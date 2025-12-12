import requests
import csv
import json

def get_city_bbox(city_name):
    """
    Get bounding box for a city using Nominatim (OSM geocoding)
    Returns (south, west, north, east)
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if not data:
        raise ValueError(f"City '{city_name}' not found")
    
    bbox = data[0]["boundingbox"]  # [south, north, west, east]
    south = float(bbox[0])
    north = float(bbox[1])
    west = float(bbox[2])
    east = float(bbox[3])
    
    return south, west, north, east


def build_full_address(tags):
    """
    Construct full address from OSM tags
    """
    housenumber = tags.get("addr:housenumber", "")
    street = tags.get("addr:street", "")
    postcode = tags.get("addr:postcode", "")
    city = tags.get("addr:city", "")
    
    parts = [street, housenumber, postcode, city]
    full_address = ", ".join([p for p in parts if p])
    return full_address or None


def fetch_restaurants(city_name):
    """
    Fetch restaurant data for a city from Overpass API
    Includes all available tags
    """
    south, west, north, east = get_city_bbox(city_name)
    
    query = f"""
    [out:json][timeout:50];
    node["amenity"="restaurant"]({south},{west},{north},{east});
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data=query)
    response.raise_for_status()
    data = response.json()
    
    restaurants = []
    
    for el in data["elements"]:
        tags = el.get("tags", {})
        lat = el.get("lat")
        lon = el.get("lon")
        name = tags.get("name")
        website = tags.get("website") or tags.get("contact:website")
        full_address = build_full_address(tags)
        country = tags.get("addr:country") or get_country(lat, lon)
        if name and lat and lon:
            restaurant_data = {
                "name": name,
                "lat": lat,
                "lon": lon,
                "website": website,
                "full_address": full_address,
                'country':country,
                'phone':tags.get("phone",None),
                'opening_hours':tags.get("opening_hours",None),
                'takeaway':tags.get("takeaway",None),
                'delivery':tags.get("delivery",None),
                
                
            }

            restaurants.append(restaurant_data)
    
    return restaurants

def get_country(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 3  # country level
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("address", {}).get("country")


def save_to_csv(restaurants, filename="restaurants.csv"):
    """
    Save restaurant data to CSV
    """
    fieldnames = ["name", "lat", "lon", "website", "full_address", "all_tags"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(restaurants)
    print(f"Saved {len(restaurants)} restaurants to {filename}")


if __name__ == "__main__":
    city_name = input("Enter city name: ").strip()
    print(f"Fetching restaurants for {city_name}...")
    
    try:
        restaurants = fetch_restaurants(city_name)
        save_to_csv(restaurants, f"{city_name.replace(' ', '_')}_ch_restaurants.csv")
    except Exception as e:
        print("Error:", e)
