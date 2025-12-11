type StringFilter = {
  label: string,
  type: "string";
  attribute: string;
  operator: "contains" | "eq";
};

type NumberFilter = {
  label: string,
  type: "number";
  attribute: string;
  operator: "gte" | "lte" | "eq";
};

export type FilterDescriptor = StringFilter | NumberFilter;


export type MenuItem = {
  id: string;
  name: string;
  cuisine_type: string | null;
  price: string | null;
  is_vegan: boolean;
  is_vegetarian: boolean;
  is_gluten_free: boolean;
  is_dairy_free: boolean;
  full_description: string | null;
};

export type Service ={
    key: string,
    value: boolean,
    category: string
}

export type WorkingHour = {
    day:string,
    from: string,
    to:string,
    is_closed:boolean
}
export type Location = {
  id: string;
  name: string;
  category?: string;
  menu_items: MenuItem[];
  latitude: string;
  longitude: string;
  booking_link?: string;
  services?: Record<string, boolean>;
  reservation_link?: string,
  order_link?:string,
  photo?:string,
  type?: string,
  price_range?: number,
  rating?: number,
  working_hours?: WorkingHour[]

};



export type FilterOptions = {
  min: number | null;
  max: number | null;
  options: string[];
}



