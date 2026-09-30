import { useMemo, useState } from "react";
import { Search, Plus, Minus, Trash2, ShoppingCart, X, PackageSearch, ShoppingBag } from "lucide-react";
import toast from "react-hot-toast";
import { useProducts } from "../../application/hooks/useProducts";
import { useCustomers } from "../../application/hooks/useCustomers";
import { useCheckout } from "../../application/hooks/useSales";
import { Card, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Select } from "../components/ui/Select";
import { Badge } from "../components/ui/Badge";
import { EmptyState } from "../components/ui/EmptyState";
import { formatCurrency } from "../../lib/formatters";
import { getErrorMessage } from "../../api/client";
import type { Product } from "../../domain/types";

interface CartLine {
  product: Product;
  quantity: number;
}

export function CheckoutPage() {
  const [search, setSearch] = useState("");
  const [cart, setCart] = useState<CartLine[]>([]);
  const [customerId, setCustomerId] = useState<string>("");

  const { data: productsPage } = useProducts({ page: 1, per_page: 50, search: search || undefined });
  const { data: customersPage } = useCustomers({ page: 1, per_page: 100 });
  const checkout = useCheckout();

  const products = productsPage?.items ?? [];
  const customers = customersPage?.items ?? [];

  const total = useMemo(
    () => cart.reduce((sum, line) => sum + line.product.price * line.quantity, 0),
    [cart]
  );

  const addToCart = (product: Product) => {
    if (product.stock_quantity <= 0) {
      toast.error("Out of stock");
      return;
    }
    setCart((prev) => {
      const existing = prev.find((l) => l.product.id === product.id);
      if (existing) {
        if (existing.quantity >= product.stock_quantity) {
          toast.error("Not enough stock");
          return prev;
        }
        return prev.map((l) =>
          l.product.id === product.id ? { ...l, quantity: l.quantity + 1 } : l
        );
      }
      return [...prev, { product, quantity: 1 }];
    });
  };

  const updateQuantity = (productId: number, delta: number) => {
    setCart((prev) =>
      prev
        .map((l) =>
          l.product.id === productId
            ? { ...l, quantity: Math.min(l.quantity + delta, l.product.stock_quantity) }
            : l
        )
        .filter((l) => l.quantity > 0)
    );
  };

  const removeLine = (productId: number) => {
    setCart((prev) => prev.filter((l) => l.product.id !== productId));
  };

  const handleCheckout = async () => {
    if (cart.length === 0) return;
    try {
      const sale = await checkout.mutateAsync({
        items: cart.map((l) => ({ product_id: l.product.id, quantity: l.quantity })),
        customer_id: customerId ? Number(customerId) : undefined,
      });
      toast.success(`Sale #${sale.id} completed — ${formatCurrency(sale.total_amount)}`);
      setCart([]);
      setCustomerId("");
    } catch (error) {
      toast.error(getErrorMessage(error, "Checkout failed"));
    }
  };

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="flex flex-col gap-4 lg:col-span-2">
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search products to add..."
            className="w-full rounded-lg border border-slate-200 bg-white py-2.5 pl-9 pr-3 text-sm outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
          />
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {products.map((product) => (
            <button
              key={product.id}
              onClick={() => addToCart(product)}
              disabled={product.stock_quantity <= 0}
              className="flex flex-col items-start gap-2 rounded-xl border border-slate-200 bg-white p-4 text-left transition-all hover:-translate-y-0.5 hover:border-brand-200 hover:shadow-lg hover:shadow-brand-500/5 disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:shadow-none"
            >
              <span className="text-sm font-medium text-slate-800 line-clamp-2">{product.name}</span>
              <span className="text-sm font-semibold text-brand-600">{formatCurrency(product.price)}</span>
              <Badge tone={product.stock_quantity <= 5 ? "warning" : "neutral"}>
                {product.stock_quantity} in stock
              </Badge>
            </button>
          ))}
          {products.length === 0 && (
            <div className="col-span-full">
              <EmptyState icon={PackageSearch} title="No products found" description="Try a different search term" />
            </div>
          )}
        </div>
      </div>

      <Card className="flex h-fit flex-col lg:sticky lg:top-0">
        <CardBody className="flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <ShoppingCart className="h-4 w-4 text-brand-600" />
            <h3 className="text-sm font-semibold text-slate-900">Current Order</h3>
          </div>

          <Select value={customerId} onChange={(e) => setCustomerId(e.target.value)}>
            <option value="">Walk-in customer</option>
            {customers.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </Select>

          <div className="flex max-h-80 flex-col gap-3 overflow-y-auto">
            {cart.length === 0 ? (
              <EmptyState icon={ShoppingBag} title="Cart is empty" description="Click a product to add it" />
            ) : (
              cart.map((line) => (
                <div key={line.product.id} className="flex items-center justify-between gap-2">
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-slate-800">{line.product.name}</p>
                    <p className="text-xs text-slate-400">{formatCurrency(line.product.price)} each</p>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => updateQuantity(line.product.id, -1)}
                      className="rounded-md border border-slate-200 p-1 text-slate-500 hover:bg-slate-50"
                    >
                      <Minus className="h-3.5 w-3.5" />
                    </button>
                    <span className="w-5 text-center text-sm font-medium">{line.quantity}</span>
                    <button
                      onClick={() => updateQuantity(line.product.id, 1)}
                      className="rounded-md border border-slate-200 p-1 text-slate-500 hover:bg-slate-50"
                    >
                      <Plus className="h-3.5 w-3.5" />
                    </button>
                    <button
                      onClick={() => removeLine(line.product.id)}
                      className="ml-1 rounded-md p-1 text-slate-400 hover:bg-red-50 hover:text-red-600"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="border-t border-slate-100 pt-4">
            <div className="mb-4 flex items-center justify-between">
              <span className="text-sm font-medium text-slate-600">Total</span>
              <span className="text-xl font-bold text-slate-900">{formatCurrency(total)}</span>
            </div>
            <div className="flex gap-2">
              {cart.length > 0 && (
                <Button variant="secondary" onClick={() => setCart([])}>
                  <X className="h-4 w-4" />
                </Button>
              )}
              <Button
                className="flex-1"
                onClick={handleCheckout}
                loading={checkout.isPending}
                disabled={cart.length === 0}
              >
                Complete Sale
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
}
