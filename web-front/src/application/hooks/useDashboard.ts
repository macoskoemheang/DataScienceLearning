import { useQuery } from "@tanstack/react-query";
import { dashboardApi } from "../../api/dashboardApi";

export function useDashboardSummary() {
  return useQuery({ queryKey: ["dashboard", "summary"], queryFn: dashboardApi.summary });
}

export function useTopProducts(limit = 5) {
  return useQuery({
    queryKey: ["dashboard", "top-products", limit],
    queryFn: () => dashboardApi.topProducts(limit),
  });
}

export function useLowStock(threshold = 5) {
  return useQuery({
    queryKey: ["dashboard", "low-stock", threshold],
    queryFn: () => dashboardApi.lowStock(threshold),
  });
}

export function useRecentSales(limit = 10) {
  return useQuery({
    queryKey: ["dashboard", "recent-sales", limit],
    queryFn: () => dashboardApi.recentSales(limit),
  });
}
