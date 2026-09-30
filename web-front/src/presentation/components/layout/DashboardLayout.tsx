import { Outlet, useLocation } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

const titles: Record<string, string> = {
  "/": "Dashboard",
  "/checkout": "Checkout",
  "/products": "Products",
  "/categories": "Categories",
  "/customers": "Customers",
  "/sales": "Sales History",
  "/employees": "Employees",
};

export function DashboardLayout() {
  const location = useLocation();
  const title = titles[location.pathname] ?? "POS Shop";

  return (
    <div className="flex h-screen w-full overflow-hidden bg-slate-50">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Topbar title={title} />
        <main key={location.pathname} className="flex-1 overflow-y-auto p-8 animate-fade-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
