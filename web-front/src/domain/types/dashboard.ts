import type { Product } from "./product";

export interface DashboardSummary {
  total_revenue: number;
  total_sales: number;
  total_products: number;
  total_customers: number;
  low_stock_count: number;
}

export interface TopProduct {
  product: Product;
  quantity_sold: number;
  revenue: number;
}
