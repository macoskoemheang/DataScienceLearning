import { useState } from "react";
import { Plus, Pencil, Trash2, Tag, Tags } from "lucide-react";
import toast from "react-hot-toast";
import {
  useCategories,
  useCreateCategory,
  useDeleteCategory,
  useUpdateCategory,
} from "../../application/hooks/useCategories";
import { useAuthStore } from "../../application/stores/authStore";
import { Card, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { Modal } from "../components/ui/Modal";
import { EmptyState } from "../components/ui/EmptyState";
import { CardSkeleton } from "../components/ui/Skeleton";
import { getErrorMessage } from "../../api/client";
import type { Category } from "../../domain/types";

interface FormState {
  name: string;
  parent_id: string;
}

const emptyForm: FormState = { name: "", parent_id: "" };

export function CategoriesPage() {
  const isAdmin = useAuthStore((s) => s.user?.role === "admin");
  const { data: categories, isLoading } = useCategories();
  const createCategory = useCreateCategory();
  const updateCategory = useUpdateCategory();
  const deleteCategory = useDeleteCategory();

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Category | null>(null);
  const [form, setForm] = useState<FormState>(emptyForm);

  const topLevel = categories?.filter((c) => c.parent_id === null) ?? [];
  const childrenOf = (parentId: number) => categories?.filter((c) => c.parent_id === parentId) ?? [];

  const openCreate = (parentId?: number) => {
    setEditing(null);
    setForm({ name: "", parent_id: parentId ? String(parentId) : "" });
    setModalOpen(true);
  };

  const openEdit = (category: Category) => {
    setEditing(category);
    setForm({ name: category.name, parent_id: category.parent_id ? String(category.parent_id) : "" });
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    const input = { name: form.name, parent_id: form.parent_id ? Number(form.parent_id) : null };
    try {
      if (editing) {
        await updateCategory.mutateAsync({ id: editing.id, input });
        toast.success("Category updated");
      } else {
        await createCategory.mutateAsync(input);
        toast.success("Category created");
      }
      setModalOpen(false);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  const handleDelete = async (category: Category) => {
    if (!confirm(`Delete "${category.name}"?`)) return;
    try {
      await deleteCategory.mutateAsync(category.id);
      toast.success("Category deleted");
    } catch (error) {
      toast.error(getErrorMessage(error, "Cannot delete this category"));
    }
  };

  // Parent options only offer top-level categories that don't already have subcategories rules
  // enforced server-side; here we just exclude the category being edited.
  const parentOptions = topLevel.filter((c) => c.id !== editing?.id);

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">
          Organize products into categories and subcategories (one level of nesting).
        </p>
        {isAdmin && (
          <Button onClick={() => openCreate()}>
            <Plus className="h-4 w-4" /> New Category
          </Button>
        )}
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <CardSkeleton key={i} className="h-24" />
          ))}
        </div>
      ) : topLevel.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {topLevel.map((category) => (
            <Card key={category.id}>
              <CardBody className="flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-50 text-brand-600">
                      <Tag className="h-4 w-4" />
                    </div>
                    <span className="text-sm font-semibold text-slate-800">{category.name}</span>
                  </div>
                  {isAdmin && (
                    <div className="flex gap-1">
                      <button
                        onClick={() => openCreate(category.id)}
                        title="Add subcategory"
                        className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                      >
                        <Plus className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => openEdit(category)}
                        className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                      >
                        <Pencil className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(category)}
                        className="rounded-lg p-1.5 text-slate-400 hover:bg-red-50 hover:text-red-600"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  )}
                </div>

                <div className="flex flex-col gap-1.5 border-t border-slate-100 pt-3">
                  {childrenOf(category.id).length === 0 ? (
                    <p className="pl-2 text-xs text-slate-400">No subcategories</p>
                  ) : (
                    childrenOf(category.id).map((child) => (
                      <div
                        key={child.id}
                        className="flex items-center justify-between rounded-lg pl-2 pr-1 py-1.5 hover:bg-slate-50"
                      >
                        <div className="flex items-center gap-2 text-sm text-slate-600">
                          <Tags className="h-3.5 w-3.5 text-slate-400" />
                          {child.name}
                        </div>
                        {isAdmin && (
                          <div className="flex gap-1">
                            <button
                              onClick={() => openEdit(child)}
                              className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
                            >
                              <Pencil className="h-3.5 w-3.5" />
                            </button>
                            <button
                              onClick={() => handleDelete(child)}
                              className="rounded-lg p-1 text-slate-400 hover:bg-red-50 hover:text-red-600"
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </button>
                          </div>
                        )}
                      </div>
                    ))
                  )}
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <EmptyState icon={Tags} title="No categories yet" description="Create your first category to start organizing products" />
        </Card>
      )}

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={editing ? "Edit Category" : form.parent_id ? "New Subcategory" : "New Category"}
      >
        <div className="flex flex-col gap-4">
          <Input label="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} autoFocus />
          <Select
            label="Parent Category (optional)"
            value={form.parent_id}
            onChange={(e) => setForm({ ...form, parent_id: e.target.value })}
            disabled={!!editing && childrenOf(editing.id).length > 0}
          >
            <option value="">None (top-level category)</option>
            {parentOptions.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </Select>
          <Button
            onClick={handleSubmit}
            loading={createCategory.isPending || updateCategory.isPending}
            className="w-full"
          >
            {editing ? "Save Changes" : "Create Category"}
          </Button>
        </div>
      </Modal>
    </div>
  );
}
