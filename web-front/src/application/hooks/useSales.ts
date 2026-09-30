import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { saleApi, type SalePageParams } from "../../api/saleApi";
import type { CheckoutInput } from "../../domain/types";

export function useSales(params: SalePageParams) {
  return useQuery({
    queryKey: ["sales", params],
    queryFn: () => saleApi.list(params),
    placeholderData: (prev) => prev,
  });
}

export function useCheckout() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: CheckoutInput) => saleApi.checkout(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["sales"] });
      queryClient.invalidateQueries({ queryKey: ["products"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}
