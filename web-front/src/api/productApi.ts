import { apiClient } from "./client";
import type { Paginated, PageParams, Product, ProductInput } from "../domain/types";

export interface ProductPageParams extends PageParams {
  category_id?: number;
}

export const productApi = {
  list: (params: ProductPageParams = {}) =>
    apiClient.get<Paginated<Product>>("/products", { params }).then((r) => r.data),

  get: (id: number) => apiClient.get<Product>(`/products/${id}`).then((r) => r.data),

  create: (input: ProductInput) => apiClient.post<Product>("/products", input).then((r) => r.data),

  update: (id: number, input: Partial<ProductInput>) =>
    apiClient.put<Product>(`/products/${id}`, input).then((r) => r.data),

  addStock: (id: number, quantity: number) =>
    apiClient.post<Product>(`/products/${id}/stock`, { quantity }).then((r) => r.data),

  remove: (id: number) => apiClient.delete(`/products/${id}`),
};
