import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { employeeApi, type EmployeeInput, type EmployeeUpdateInput } from "../../api/employeeApi";

export function useEmployees() {
  return useQuery({
    queryKey: ["employees"],
    queryFn: () => employeeApi.list(),
  });
}

export function useCreateEmployee() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: EmployeeInput) => employeeApi.create(input),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["employees"] }),
  });
}

export function useUpdateEmployee() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, input }: { id: number; input: EmployeeUpdateInput }) =>
      employeeApi.update(id, input),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["employees"] }),
  });
}
