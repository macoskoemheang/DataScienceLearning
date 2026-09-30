import { LogOut, User as UserIcon } from "lucide-react";
import { useAuthStore } from "../../../application/stores/authStore";
import { useLogout } from "../../../application/hooks/useAuth";
import { Badge } from "../ui/Badge";

export function Topbar({ title }: { title: string }) {
  const user = useAuthStore((s) => s.user);
  const logout = useLogout();

  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 bg-white px-8">
      <h1 className="text-lg font-semibold text-slate-900">{title}</h1>

      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-50 text-brand-600">
              <UserIcon className="h-4 w-4" />
            </div>
            <div className="text-sm">
              <p className="font-medium text-slate-800">{user.username}</p>
            </div>
            <Badge tone={user.role === "admin" ? "brand" : "neutral"}>{user.role}</Badge>
          </div>
        )}
        <button
          onClick={logout}
          className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-slate-500 hover:bg-slate-100 hover:text-slate-700"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </button>
      </div>
    </header>
  );
}
