export interface SaleItem {
  id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  subtotal: number;
}

export interface Sale {
  id: number;
  employee_id: number;
  customer_id: number | null;
  items: SaleItem[];
  total_amount: number;
  created_at: string;
}

export interface CheckoutItemInput {
  product_id: number;
  quantity: number;
}

export interface CheckoutInput {
  items: CheckoutItemInput[];
  customer_id?: number | null;
}
