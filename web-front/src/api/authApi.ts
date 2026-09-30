import { apiClient } from "./client";
import type { LoginResponse, User } from "../domain/types";

export const authApi = {
  login: (username: string, password: string) =>
    apiClient.post<LoginResponse>("/auth/login", { username, password }).then((r) => r.data),

  register: (username: string, password: string) =>
    apiClient.post<User>("/auth/register", { username, password }).then((r) => r.data),

  me: () => apiClient.get<User>("/auth/me").then((r) => r.data),
};
