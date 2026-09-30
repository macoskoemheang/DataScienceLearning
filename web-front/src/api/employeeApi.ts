import { apiClient } from "./client";
import type { Role, User } from "../domain/types";

export interface EmployeeInput {
  username: string;
  password: string;
  role: Role;
}

export interface EmployeeUpdateInput {
  role?: Role;
  is_active?: boolean;
}

export const employeeApi = {
  list: () => apiClient.get<User[]>("/employees").then((r) => r.data),

  create: (input: EmployeeInput) => apiClient.post<User>("/employees", input).then((r) => r.data),

  update: (id: number, input: EmployeeUpdateInput) =>
    apiClient.put<User>(`/employees/${id}`, input).then((r) => r.data),
};
