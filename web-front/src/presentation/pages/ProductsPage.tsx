import { useState } from "react";
import { Plus, Search, Pencil, Trash2, PackagePlus, Package } from "lucide-react";
import toast from "react-hot-toast";
import {
  useAddStock,
  useCreateProduct,
  useDeleteProduct,
  useProducts,
  useUpdateProduct,
} from "../../application/hooks/useProducts";
import { useCategories } from "../../application/hooks/useCategories";
import { useAuthStore } from "../../application/stores/authStore";
import { Card } from "../components/ui/Card";
import { Table, type Column } from "../components/ui/Table";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { Modal } from "../components/ui/Modal";
import { Pagination } from "../components/ui/Pagination";
import { Badge } from "../components/ui/Badge";
import { formatCurrency } from "../../lib/formatters";
import { getErrorMessage } from "../../api/client";
import type { Category, Product } from "../../domain/types";

const PER_PAGE = 10;

interface ProductFormState {
  name: string;
  sku: string;
  price: string;
  stock_quantity: string;
  category_id: string;
}

const emptyForm: ProductFormState = { name: "", sku: "", price: "", stock_quantity: "0", category_id: "" };

/** Top-level categories followed immediately by their subcategories, for a grouped <select>. */
function buildCategoryOptions(categories: Category[] | undefined) {
  if (!categories) return [];
  const topLevel = categories.filter((c) => c.parent_id === null);
  const options: { id: number; label: string }[] = [];
  for (const parent of topLevel) {
    options.push({ id: parent.id, label: parent.name });
    for (const child of categories.filter((c) => c.parent_id === parent.id)) {
      options.push({ id: child.id, label: `— ${child.name}` });
    }
  }
  return options;
}

export function ProductsPage() {
  const isAdmin = useAuthStore((s) => s.user?.role === "admin");
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Product | null>(null);
  const [form, setForm] = useState<ProductFormState>(emptyForm);
  const [stockModalProduct, setStockModalProduct] = useState<Product | null>(null);
  const [stockAmount, setStockAmount] = useState("");

  const { data, isLoading } = useProducts({ page, per_page: PER_PAGE, search: search || undefined });
  const { data: categories } = useCategories();
  const createProduct = useCreateProduct();
  const updateProduct = useUpdateProduct();
  const deleteProduct = useDeleteProduct();
  const addStock = useAddStock();

  const categoryOptions = buildCategoryOptions(categories);

  const openCreate = () => {
    setEditing(null);
    setForm(emptyForm);
    setModalOpen(true);
  };

  const openEdit = (product: Product) => {
    setEditing(product);
    setForm({
      name: product.name,
      sku: product.sku,
      price: String(product.price),
      stock_quantity: String(product.stock_quantity),
      category_id: product.category_id ? String(product.category_id) : "",
    });
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    const input = {
      name: form.name,
      sku: form.sku,
      price: Number(form.price),
      stock_quantity: Number(form.stock_quantity),
      category_id: form.category_id ? Number(form.category_id) : null,
    };
    try {
      if (editing) {
        await updateProduct.mutateAsync({ id: editing.id, input });
        toast.success("Product updated");
      } else {
        await createProduct.mutateAsync(input);
        toast.success("Product created");
      }
      setModalOpen(false);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const handleDelete = async (product: Product) => {
    if (!confirm(`Delete "${product.name}"?`)) return;
    try {
      await deleteProduct.mutateAsync(product.id);
      toast.success("Product deleted");
    } catch (error) {
      toast.error(getErrorMessage(error, "Cannot delete this product"));
    }
  };

  const openStockModal = (product: Product) => {
    setStockModalProduct(product);
    setStockAmount("");
  };

  const handleAddStock = async () => {
    if (!stockModalProduct) return;
    const quantity = Number(stockAmount);
    try {
      const updated = await addStock.mutateAsync({ id: stockModalProduct.id, quantity });
      toast.success(`Added ${quantity} units — new stock: ${updated.stock_quantity}`);
      setStockModalProduct(null);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const categoryName = (id: number | null) => {
    if (id === null) return "—";
    const category = categories?.find((c) => c.id === id);
    if (!category) return "—";
    if (category.parent_id === null) return category.name;
    const parent = categories?.find((c) => c.id === category.parent_id);
    return parent ? `${parent.name} › ${category.name}` : category.name;
  };

  const columns: Column<Product>[] = [
    { header: "Name", accessor: (p) => <span className="font-medium text-slate-800">{p.name}</span> },
    { header: "SKU", accessor: (p) => p.sku || "—" },
    { header: "Category", accessor: (p) => categoryName(p.category_id) },
    { header: "Price", accessor: (p) => formatCurrency(p.price) },
    {
      header: "Stock",
      accessor: (p) => (
        <Badge tone={p.stock_quantity <= 5 ? "warning" : "success"}>{p.stock_quantity}</Badge>
      ),
    },
    ...(isAdmin
      ? [
          {
            header: "",
            accessor: (p: Product) => (
              <div className="flex justify-end gap-1">
                <button
                  onClick={() => openStockModal(p)}
                  title="Add stock"
                  className="rounded-lg p-1.5 text-slate-400 hover:bg-emerald-50 hover:text-emerald-600"
                >
                  <PackagePlus className="h-4 w-4" />
                </button>
                <button
                  onClick={() => openEdit(p)}
                  className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                >
                  <Pencil className="h-4 w-4" />
                </button>
                <button
                  onClick={() => handleDelete(p)}
                  className="rounded-lg p-1.5 text-slate-400 hover:bg-red-50 hover:text-red-600"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            ),
            className: "text-right",
          },
        ]
      : []),
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
            placeholder="Search products..."
            className="w-full rounded-lg border border-slate-200 bg-white py-2.5 pl-9 pr-3 text-sm outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20"
          />
        </div>
        {isAdmin && (
          <Button onClick={openCreate}>
            <Plus className="h-4 w-4" /> New Product
          </Button>
        )}
      </div>

      <Card>
        <Table
          columns={columns}
          data={data?.items ?? []}
          rowKey={(p) => p.id}
          loading={isLoading}
          emptyIcon={Package}
          emptyMessage={search ? "No products match your search" : "No products yet"}
        />
        {data && !isLoading && (
          <Pagination page={page} perPage={PER_PAGE} total={data.total} onPageChange={setPage} />
        )}
      </Card>

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? "Edit Product" : "New Product"}>
        <div className="flex flex-col gap-4">
          <Input
            label="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <Input
            label="SKU"
            value={form.sku}
            onChange={(e) => setForm({ ...form, sku: e.target.value })}
          />
          <div className="grid grid-cols-2 gap-3">
            <Input
              label="Price"
              type="number"
              step="0.01"
              value={form.price}
              onChange={(e) => setForm({ ...form, price: e.target.value })}
            />
            <Input
              label="Stock Quantity"
              type="number"
              value={form.stock_quantity}
              onChange={(e) => setForm({ ...form, stock_quantity: e.target.value })}
            />
          </div>
          <Select
            label="Category"
            value={form.category_id}
            onChange={(e) => setForm({ ...form, category_id: e.target.value })}
          >
            <option value="">No category</option>
            {categoryOptions.map((c) => (
              <option key={c.id} value={c.id}>
                {c.label}
              </option>
            ))}
          </Select>
          <Button
            onClick={handleSubmit}
            loading={createProduct.isPending || updateProduct.isPending}
            className="mt-1 w-full"
          >
            {editing ? "Save Changes" : "Create Product"}
          </Button>
        </div>
      </Modal>

      <Modal
        open={!!stockModalProduct}
        onClose={() => setStockModalProduct(null)}
        title={`Add Stock — ${stockModalProduct?.name ?? ""}`}
      >
        <div className="flex flex-col gap-4">
          <p className="text-sm text-slate-500">
            Current stock: <span className="font-medium text-slate-800">{stockModalProduct?.stock_quantity}</span>
          </p>
          <Input
            label="Quantity to add"
            type="number"
            min={1}
            value={stockAmount}
            onChange={(e) => setStockAmount(e.target.value)}
            placeholder="e.g. 50"
            autoFocus
          />
          <Button onClick={handleAddStock} loading={addStock.isPending} className="w-full">
            Add Stock
          </Button>
        </div>
      </Modal>
    </div>
  );
}
