import { useState } from "react";
import { Plus, Search, Pencil, Users } from "lucide-react";
import toast from "react-hot-toast";
import {
  useCreateCustomer,
  useCustomers,
  useUpdateCustomer,
} from "../../application/hooks/useCustomers";
import { Card } from "../components/ui/Card";
import { Table, type Column } from "../components/ui/Table";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Modal } from "../components/ui/Modal";
import { Pagination } from "../components/ui/Pagination";
import { getErrorMessage } from "../../api/client";
import type { Customer } from "../../domain/types";

const PER_PAGE = 10;
const emptyForm = { name: "", phone: "", email: "" };

export function CustomersPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Customer | null>(null);
  const [form, setForm] = useState(emptyForm);

  const { data, isLoading } = useCustomers({ page, per_page: PER_PAGE, search: search || undefined });
  const createCustomer = useCreateCustomer();
  const updateCustomer = useUpdateCustomer();

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setModalOpen(true);
  };

  const openEdit = (customer: Customer) => {
    setEditing(customer);
    setForm({ name: customer.name, phone: customer.phone, email: customer.email });
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    try {
      if (editing) {
        await updateCustomer.mutateAsync({ id: editing.id, input: form });
        toast.success("Customer updated");
      } else {
        await createCustomer.mutateAsync(form);
        toast.success("Customer created");
      }
      setModalOpen(false);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const columns: Column<Customer>[] = [
    { header: "Name", accessor: (c) => <span className="font-medium text-slate-800">{c.name}</span> },
    { header: "Phone", accessor: (c) => c.phone || "—" },
    { header: "Email", accessor: (c) => c.email || "—" },
    {
      header: "",
      accessor: (c) => (
        <div className="flex justify-end">
          <button
            onClick={() => openEdit(c)}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
          >
            <Pencil className="h-4 w-4" />
          </button>
        </div>
      ),
      className: "text-right",
    },
  ];

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <div className="relative w-72">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search customers..."
            className="w-full rounded-lg border border-slate-200 bg-white py-2.5 pl-9 pr-3 text-sm outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
          />
        </div>
        <Button onClick={openCreate}>
          <Plus className="h-4 w-4" /> New Customer
        </Button>
      </div>

      <Card>
        <Table
          columns={columns}
          data={data?.items ?? []}
          rowKey={(c) => c.id}
          loading={isLoading}
          emptyIcon={Users}
          emptyMessage={search ? "No customers match your search" : "No customers yet"}
        />
        {data && !isLoading && (
          <Pagination page={page} perPage={PER_PAGE} total={data.total} onPageChange={setPage} />
        )}
      </Card>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? "Edit Customer" : "New Customer"}>
        <div className="flex flex-col gap-4">
          <Input label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} autoFocus />
          <Input label="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <Input label="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <Button
            onClick={handleSubmit}
            loading={createCustomer.isPending || updateCustomer.isPending}
            className="w-full"
          >
            {editing ? "Save Changes" : "Create Customer"}
          </Button>
        </div>
      </Modal>
    </div>
  );
}
