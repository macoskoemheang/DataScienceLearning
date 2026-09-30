import { useState } from "react";
import { Plus, ShieldCheck, ShieldOff, UserCog } from "lucide-react";
import toast from "react-hot-toast";
import {
  useCreateEmployee,
  useEmployees,
  useUpdateEmployee,
} from "../../application/hooks/useEmployees";
import { useAuthStore } from "../../application/stores/authStore";
import { Card } from "../components/ui/Card";
import { Table, type Column } from "../components/ui/Table";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { Modal } from "../components/ui/Modal";
import { Badge } from "../components/ui/Badge";
import { getErrorMessage } from "../../api/client";
import type { Role, User } from "../../domain/types";

const emptyForm = { username: "", password: "", role: "cashier" as Role };

export function EmployeesPage() {
  const currentUserId = useAuthStore((s) => s.user?.id);
  const { data: employees, isLoading } = useEmployees();
  const createEmployee = useCreateEmployee();
  const updateEmployee = useUpdateEmployee();

  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState(emptyForm);

  const handleCreate = async () => {
    try {
      await createEmployee.mutateAsync(form);
      toast.success("Employee created");
      setModalOpen(false);
      setForm(emptyForm);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const toggleActive = async (employee: User) => {
    try {
      await updateEmployee.mutateAsync({ id: employee.id, input: { is_active: !employee.is_active } });
      toast.success(employee.is_active ? "Employee deactivated" : "Employee reactivated");
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const changeRole = async (employee: User, role: Role) => {
    try {
      await updateEmployee.mutateAsync({ id: employee.id, input: { role } });
      toast.success("Role updated");
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const columns: Column<User>[] = [
    { header: "Username", accessor: (u) => <span className="font-medium text-slate-800">{u.username}</span> },
    {
      header: "Role",
      accessor: (u) =>
        u.id === currentUserId ? (
          <Badge tone="brand">{u.role}</Badge>
        ) : (
          <select
            value={u.role}
            onChange={(e) => changeRole(u, e.target.value as Role)}
            className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs outline-none focus:border-brand-500"
          >
            <option value="cashier">cashier</option>
            <option value="admin">admin</option>
          </select>
        ),
    },
    {
      header: "Status",
      accessor: (u) => <Badge tone={u.is_active ? "success" : "danger"}>{u.is_active ? "Active" : "Inactive"}</Badge>,
    },
    {
      header: "",
      accessor: (u) =>
        u.id === currentUserId ? (
          <span className="text-xs text-slate-400">This is you</span>
        ) : (
          <div className="flex justify-end">
            <button
              onClick={() => toggleActive(u)}
              className={`flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs font-medium ${
                u.is_active
                  ? "text-red-600 hover:bg-red-50"
                  : "text-emerald-600 hover:bg-emerald-50"
              }`}
            >
              {u.is_active ? <ShieldOff className="h-3.5 w-3.5" /> : <ShieldCheck className="h-3.5 w-3.5" />}
              {u.is_active ? "Deactivate" : "Reactivate"}
            </button>
          </div>
        ),
      className: "text-right",
    },
  ];

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">Manage staff accounts and permissions.</p>
        <Button onClick={() => setModalOpen(true)}>
          <Plus className="h-4 w-4" /> New Employee
        </Button>
      </div>

      <Card>
        <Table
          columns={columns}
          data={employees ?? []}
          rowKey={(u) => u.id}
          loading={isLoading}
          emptyIcon={UserCog}
          emptyMessage="No employees yet"
        />
      </Card>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="New Employee">
        <div className="flex flex-col gap-4">
          <Input
            label="Username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            autoFocus
          />
          <Input
            label="Password"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <Select
            label="Role"
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value as Role })}
          >
            <option value="cashier">Cashier</option>
            <option value="admin">Admin</option>
          </Select>
          <Button onClick={handleCreate} loading={createEmployee.isPending} className="w-full">
            Create Employee
          </Button>
        </div>
      </Modal>
    </div>
  );
}
