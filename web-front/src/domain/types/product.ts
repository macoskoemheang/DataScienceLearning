export interface Category {
  id: number;
  name: string;
  parent_id: number | null;
}

export interface CategoryInput {
  name: string;
  parent_id?: number | null;
}

export interface Product {
  id: number;
  name: string;
  sku: string;
  price: number;
  stock_quantity: number;
  category_id: number | null;
  created_at: string;
}

export interface ProductInput {
  name: string;
  price: number;
  sku?: string;
  stock_quantity?: number;
  category_id?: number | null;
}
