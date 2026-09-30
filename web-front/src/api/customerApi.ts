import { apiClient } from "./client";
import type { Customer, CustomerInput, PageParams, Paginated } from "../domain/types";

export const customerApi = {
  list: (params: PageParams = {}) =>
    apiClient.get<Paginated<Customer>>("/customers", { params }).then((r) => r.data),

  get: (id: number) => apiClient.get<Customer>(`/customers/${id}`).then((r) => r.data),

  create: (input: CustomerInput) => apiClient.post<Customer>("/customers", input).then((r) => r.data),

  update: (id: number, input: Partial<CustomerInput>) =>
    apiClient.put<Customer>(`/customers/${id}`, input).then((r) => r.data),
};
