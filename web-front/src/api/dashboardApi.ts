import { apiClient } from "./client";
import type { DashboardSummary, Product, Sale, TopProduct } from "../domain/types";

export const dashboardApi = {
  summary: () => apiClient.get<DashboardSummary>("/dashboard/summary").then((r) => r.data),

  topProducts: (limit = 5) =>
    apiClient
      .get<TopProduct[]>("/dashboard/top-products", { params: { limit } })
      .then((r) => r.data),

  lowStock: (threshold = 5) =>
    apiClient
      .get<Product[]>("/dashboard/low-stock", { params: { threshold } })
      .then((r) => r.data),

  recentSales: (limit = 10) =>
    apiClient.get<Sale[]>("/dashboard/recent-sales", { params: { limit } }).then((r) => r.data),
};
