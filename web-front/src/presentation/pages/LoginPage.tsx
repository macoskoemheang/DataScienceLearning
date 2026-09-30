import { type FormEvent, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Store } from "lucide-react";
import toast from "react-hot-toast";
import { useLogin, useRegister } from "../../application/hooks/useAuth";
import { useAuthStore } from "../../application/stores/authStore";
import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";
import { getErrorMessage } from "../../api/client";
import clsx from "clsx";

export function LoginPage() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const navigate = useNavigate();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = useLogin();
  const register = useRegister();

  if (accessToken) return <Navigate to="/" replace />;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      if (mode === "login") {
        await login.mutateAsync({ username, password });
        navigate("/", { replace: true });
      } else {
        await register.mutateAsync({ username, password });
        toast.success("Account created — you can log in now");
        setMode("login");
      }
    } catch (error) {
      toast.error(getErrorMessage(error, "Something went wrong"));
    }
  };

  const isLoading = login.isPending || register.isPending;

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-gradient-to-br from-slate-900 via-slate-900 to-brand-900 px-4">
      <div className="pointer-events-none absolute -left-32 -top-32 h-96 w-96 rounded-full bg-brand-500/20 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-32 -right-32 h-96 w-96 rounded-full bg-violet-500/20 blur-3xl" />
      <div className="pointer-events-none absolute left-1/2 top-1/2 h-64 w-64 -translate-x-1/2 -translate-y-1/2 rounded-full bg-brand-400/10 blur-3xl" />

      <div className="relative w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center gap-3 text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-500/20 text-brand-300 ring-1 ring-brand-400/30">
            <Store className="h-7 w-7" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-white">POS Shop</h1>
            <p className="text-sm text-slate-400">Management Console</p>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-2xl shadow-black/20">
          <div className="mb-5 flex rounded-lg bg-slate-100 p-1">
            {(["login", "register"] as const).map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={clsx(
                  "flex-1 rounded-md py-2 text-sm font-medium capitalize transition-colors",
                  mode === m ? "bg-white text-slate-900 shadow-sm" : "text-slate-500"
                )}
              >
                {m}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <Input
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="owner"
              autoFocus
              required
            />
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
            <Button type="submit" loading={isLoading} className="mt-1 w-full">
              {mode === "login" ? "Sign in" : "Create account"}
            </Button>
          </form>

          {mode === "register" && (
            <p className="mt-4 text-center text-xs text-slate-400">
              The very first account created becomes an admin automatically.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
