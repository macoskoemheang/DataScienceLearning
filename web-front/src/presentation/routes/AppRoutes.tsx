import { Routes, Route } from "react-router-dom";
import { LoginPage } from "../pages/LoginPage";
import { DashboardPage } from "../pages/DashboardPage";
import { ProductsPage } from "../pages/ProductsPage";
import { CategoriesPage } from "../pages/CategoriesPage";
import { CustomersPage } from "../pages/CustomersPage";
import { CheckoutPage } from "../pages/CheckoutPage";
import { SalesHistoryPage } from "../pages/SalesHistoryPage";
import { EmployeesPage } from "../pages/EmployeesPage";
import { DashboardLayout } from "../components/layout/DashboardLayout";
import { AdminRoute, ProtectedRoute } from "./ProtectedRoute";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="checkout" element={<CheckoutPage />} />
          <Route path="products" element={<ProductsPage />} />
          <Route path="categories" element={<CategoriesPage />} />
          <Route path="customers" element={<CustomersPage />} />
          <Route path="sales" element={<SalesHistoryPage />} />
          <Route element={<AdminRoute />}>
            <Route path="employees" element={<EmployeesPage />} />
          </Route>
        </Route>
      </Route>
    </Routes>
  );
}
