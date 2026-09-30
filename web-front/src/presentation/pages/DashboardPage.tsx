import { DollarSign, Receipt, Package, Users, AlertTriangle, CheckCircle2, ShoppingBag } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  useDashboardSummary,
  useLowStock,
  useRecentSales,
  useTopProducts,
} from "../../application/hooks/useDashboard";
import { useAuthStore } from "../../application/stores/authStore";
import { Card, CardBody, CardHeader, CardTitle } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { EmptyState } from "../components/ui/EmptyState";
import { CardSkeleton, Skeleton } from "../components/ui/Skeleton";
import { formatCurrency, formatDate } from "../../lib/formatters";

const statCards = [
  {
    key: "total_revenue" as const,
    label: "Total Revenue",
    icon: DollarSign,
    format: formatCurrency,
    iconBg: "bg-emerald-500",
    ring: "ring-emerald-500/10",
  },
  {
    key: "total_sales" as const,
    label: "Total Sales",
    icon: Receipt,
    format: (v: number) => v.toString(),
    iconBg: "bg-blue-500",
    ring: "ring-blue-500/10",
  },
  {
    key: "total_products" as const,
    label: "Products",
    icon: Package,
    format: (v: number) => v.toString(),
    iconBg: "bg-violet-500",
    ring: "ring-violet-500/10",
  },
  {
    key: "total_customers" as const,
    label: "Customers",
    icon: Users,
    format: (v: number) => v.toString(),
    iconBg: "bg-amber-500",
    ring: "ring-amber-500/10",
  },
];

const todayLabel = new Date().toLocaleDateString(undefined, {
  weekday: "long",
  month: "long",
  day: "numeric",
});

export function DashboardPage() {
  const username = useAuthStore((s) => s.user?.username);
  const { data: summary, isLoading } = useDashboardSummary();
  const { data: topProducts } = useTopProducts(5);
  const { data: lowStock } = useLowStock(5);
  const { data: recentSales } = useRecentSales(6);

  const chartData = (topProducts ?? []).map((tp) => ({
    name: tp.product.name,
    sold: tp.quantity_sold,
  }));

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h2 className="text-xl font-semibold text-slate-900">
          Welcome back{username ? `, ${username}` : ""} 👋
        </h2>
        <p className="text-sm text-slate-500">{todayLabel}</p>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {isLoading || !summary
          ? Array.from({ length: 4 }).map((_, i) => <CardSkeleton key={i} />)
          : statCards.map((card) => (
              <Card key={card.key} className="relative overflow-hidden">
                <CardBody className="flex items-center gap-4">
                  <div
                    className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl ${card.iconBg} text-white shadow-lg ring-8 ${card.ring}`}
                  >
                    <card.icon className="h-5 w-5" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-xs font-medium text-slate-500">{card.label}</p>
                    <p className="truncate text-2xl font-bold tracking-tight text-slate-900">
                      {card.format(summary[card.key])}
                    </p>
                  </div>
                </CardBody>
              </Card>
            ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Top-Selling Products</CardTitle>
          </CardHeader>
          <CardBody>
            {isLoading ? (
              <Skeleton className="h-64 w-full rounded-xl" />
            ) : chartData.length === 0 ? (
              <EmptyState icon={ShoppingBag} title="No sales yet" description="Completed sales will show up here" />
            ) : (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={chartData} margin={{ left: -20 }}>
                  <defs>
                    <linearGradient id="barFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#818cf8" />
                      <stop offset="100%" stopColor="#4f46e5" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: "#64748b" }} />
                  <YAxis tick={{ fontSize: 12, fill: "#64748b" }} allowDecimals={false} />
                  <Tooltip
                    cursor={{ fill: "#f8fafc" }}
                    contentStyle={{ borderRadius: 10, border: "1px solid #e2e8f0", fontSize: 13 }}
                  />
                  <Bar dataKey="sold" fill="url(#barFill)" radius={[6, 6, 0, 0]} name="Units sold" maxBarSize={56} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Low Stock Alerts</CardTitle>
          </CardHeader>
          <CardBody className="flex flex-col gap-3">
            {isLoading ? (
              <div className="flex flex-col gap-2">
                {Array.from({ length: 3 }).map((_, i) => (
                  <Skeleton key={i} className="h-11 w-full rounded-lg" />
                ))}
              </div>
            ) : !lowStock || lowStock.length === 0 ? (
              <div className="flex flex-col items-center gap-2 py-8 text-center">
                <CheckCircle2 className="h-8 w-8 text-emerald-500" />
                <p className="text-sm font-medium text-slate-600">All stocked up</p>
              </div>
            ) : (
              lowStock.map((product) => (
                <div
                  key={product.id}
                  className="flex items-center justify-between rounded-lg bg-amber-50/60 px-3 py-2.5"
                >
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                    <span className="text-sm font-medium text-slate-700">{product.name}</span>
                  </div>
                  <Badge tone="warning">{product.stock_quantity} left</Badge>
                </div>
              ))
            )}
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Sales</CardTitle>
        </CardHeader>
        <CardBody className="p-0">
          {isLoading ? (
            <div className="flex flex-col gap-0 p-5">
              {Array.from({ length: 3 }).map((_, i) => (
                <Skeleton key={i} className="mb-3 h-12 w-full rounded-lg last:mb-0" />
              ))}
            </div>
          ) : !recentSales || recentSales.length === 0 ? (
            <EmptyState icon={Receipt} title="No sales yet" description="Sales from Checkout will appear here" />
          ) : (
            <div className="divide-y divide-slate-50">
              {recentSales.map((sale) => (
                <div key={sale.id} className="flex items-center gap-4 px-5 py-3.5">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-brand-50 text-xs font-semibold text-brand-600">
                    #{sale.id}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-slate-800">Sale #{sale.id}</p>
                    <p className="text-xs text-slate-400">{formatDate(sale.created_at)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-slate-900">
                      {formatCurrency(sale.total_amount)}
                    </p>
                    <p className="text-xs text-slate-400">{sale.items.length} item(s)</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
