import { apiClient } from "./client";
import type { Category, CategoryInput } from "../domain/types";

export const categoryApi = {
  list: () => apiClient.get<Category[]>("/categories").then((r) => r.data),

  create: (input: CategoryInput) =>
    apiClient.post<Category>("/categories", input).then((r) => r.data),

  update: (id: number, input: Partial<CategoryInput>) =>
    apiClient.put<Category>(`/categories/${id}`, input).then((r) => r.data),

  remove: (id: number) => apiClient.delete(`/categories/${id}`),
};
