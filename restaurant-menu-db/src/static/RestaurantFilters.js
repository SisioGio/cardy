



export const restaurantFilters = {

  'restaurant':{

      // rest_name: {
      //     label: "Restaurant Name",
      //     type: "string",
      //     attribute: "name",
      //     operator: "contains",
      //   },

      rest_rating: {
        label: "Rating (min)",
        type: "number",
        attribute: "rating",
        operator: "gte"
      },
      
      rest_price_range: {
        label: "Price Range",
        type: "number",
        attribute: "price_range",
        operator: "eq",
      },
      rest_sub_type: {
        label: "Subtype",
        type: "string",
        attribute: "subtypes",
        operator: "contains",
      },
      // rest_type: {
      //   label: "Type",
      //   type: "string",
      //   attribute: "type",
      //   operator: "contains",
      // },
  },

  'menu': {
    // item_name: {
    //   label: "Name",
    //   type: "string",
    //   attribute: "name",
    //   operator: "ilike",
    // },
    cuisine_type: {
      label: "Cuisine Type",
      type: "string",
      attribute: "cuisine_type",
      operator: "ilike",
    },
    

    spiciness_level: {
      label: "Spiciness Level",
      type: "string",
      attribute: "spiciness_level",
      operator: "ilike",
    },
    is_vegan: {
      label: "Vegan",
      type: "bool",
      attribute: "is_vegan",
      operator: "eq",
    },
    is_vegetarian: {
      label: "Vegetarian",
      type: "bool",
      attribute: "is_vegetarian",
      operator: "eq",
    },
    is_gluten_free: {
      label: "Gluten Free",
      type: "bool",
      attribute: "is_gluten_free",
      operator: "eq",
    },
    is_dairy_free: {
      label: "Dairy Free",
      type: "bool",
      attribute: "is_dairy_free",
      operator: "eq",
    },
    is_low_carb: {
      label: "Low Carb",
      type: "bool",
      attribute: "is_low_carb",
      operator: "eq",
    },
    is_nut_free: {
      label: "Nut Free",
      type: "bool",
      attribute: "is_nut_free",
      operator: "eq",
    },
    // price_min: {
    //   label: "Minimum Price",
    //   type: "number",
    //   attribute: "price",
    //   operator: "range",
    // },
    // price_max: {
    //   label: "Maximum Price",
    //   type: "number",
    //   attribute: "price",
    //   operator: "range",
    // },
    calories: {
      label: "Calories",
      type: "number",
      attribute: "calories",
      operator: "range",
    },
    carbs: {
      label: "Carbs",
      type: "number",
      attribute: "carbs",
      operator: "range",
    },
    proteins: {
      label: "Proteins",
      type: "number",
      attribute: "proteins",
      operator: "range",
    },
    fat: {
      label: "Fat",
      type: "number",
      attribute: "fat",
      operator: "range",
    },
    fiber: {
      label: "Fiber",
      type: "number",
      attribute: "fiber",
      operator: "range",
    },
    sugar: {
      label: "Sugar",
      type: "number",
      attribute: "sugar",
      operator: "range",
    },
    sodium: {
      label: "Sodium",
      type: "number",
      attribute: "sodium",
      operator: "range",
    },
  },
  

    'services':{

      service_key: {
          label: "Service",
          type: "string",
          attribute: "key",
          operator: "eq",
        }
  },
};
