import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../../application/stores/authStore";
import { useCurrentUser } from "../../application/hooks/useAuth";
import { FullPageSpinner } from "../components/ui/Spinner";

export function ProtectedRoute() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const { isLoading, isError } = useCurrentUser();

  if (!accessToken) return <Navigate to="/login" replace />;
  if (isLoading) return <FullPageSpinner />;
  if (isError) return <Navigate to="/login" replace />;

  return <Outlet />;
}

export function AdminRoute() {
  const role = useAuthStore((s) => s.user?.role);
  if (role !== "admin") return <Navigate to="/" replace />;
  return <Outlet />;
}
