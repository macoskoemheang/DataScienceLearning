import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { customerApi } from "../../api/customerApi";
import type { CustomerInput, PageParams } from "../../domain/types";

export function useCustomers(params: PageParams) {
  return useQuery({
    queryKey: ["customers", params],
    queryFn: () => customerApi.list(params),
    placeholderData: (prev) => prev,
  });
}

export function useCreateCustomer() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: CustomerInput) => customerApi.create(input),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["customers"] }),
  });
}

export function useUpdateCustomer() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, input }: { id: number; input: Partial<CustomerInput> }) =>
      customerApi.update(id, input),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["customers"] }),
  });
}
