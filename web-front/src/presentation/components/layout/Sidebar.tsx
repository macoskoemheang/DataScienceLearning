import { NavLink } from "react-router-dom";
import clsx from "clsx";
import {
  LayoutDashboard,
  ShoppingCart,
  Package,
  Tags,
  Users,
  Receipt,
  UserCog,
  Store,
} from "lucide-react";
import { useAuthStore } from "../../../application/stores/authStore";

interface NavItem {
  to: string;
  label: string;
  icon: typeof LayoutDashboard;
  adminOnly?: boolean;
}

const navItems: NavItem[] = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/checkout", label: "Checkout", icon: ShoppingCart },
  { to: "/products", label: "Products", icon: Package },
  { to: "/categories", label: "Categories", icon: Tags },
  { to: "/customers", label: "Customers", icon: Users },
  { to: "/sales", label: "Sales History", icon: Receipt },
  { to: "/employees", label: "Employees", icon: UserCog, adminOnly: true },
];

export function Sidebar() {
  const role = useAuthStore((s) => s.user?.role);

  return (
    <aside className="flex h-full w-64 shrink-0 flex-col bg-slate-900 text-slate-300">
      <div className="flex items-center gap-2 px-6 py-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-500/20 text-brand-400">
          <Store className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-semibold text-white">POS Shop</p>
          <p className="text-xs text-slate-500">Management Console</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3">
        {navItems
          .filter((item) => !item.adminOnly || role === "admin")
          .map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                clsx(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-brand-600 text-white shadow-sm shadow-brand-600/30"
                    : "text-slate-400 hover:bg-slate-800 hover:text-white"
                )
              }
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          ))}
      </nav>

      <div className="px-6 py-4 text-xs text-slate-600">v1.0.0</div>
    </aside>
  );
}
