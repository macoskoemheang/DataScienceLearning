import { apiClient } from "./client";
import type { CheckoutInput, PageParams, Paginated, Sale } from "../domain/types";

export interface SalePageParams extends PageParams {
  start_date?: string;
  end_date?: string;
}

export const saleApi = {
  list: (params: SalePageParams = {}) =>
    apiClient.get<Paginated<Sale>>("/sales", { params }).then((r) => r.data),

  get: (id: number) => apiClient.get<Sale>(`/sales/${id}`).then((r) => r.data),

  checkout: (input: CheckoutInput) =>
    apiClient.post<Sale>("/sales/checkout", input).then((r) => r.data),
};
