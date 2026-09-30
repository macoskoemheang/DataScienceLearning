import type { ReactNode } from "react";
import clsx from "clsx";
import type { LucideIcon } from "lucide-react";
import { Inbox } from "lucide-react";
import { EmptyState } from "./EmptyState";
import { TableSkeleton } from "./Skeleton";

export interface Column<T> {
  header: string;
  accessor: (row: T) => ReactNode;
  className?: string;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  rowKey: (row: T) => string | number;
  emptyMessage?: string;
  emptyIcon?: LucideIcon;
  loading?: boolean;
}

export function Table<T>({
  columns,
  data,
  rowKey,
  emptyMessage = "No records found",
  emptyIcon = Inbox,
  loading = false,
}: TableProps<T>) {
  if (loading) {
    return <TableSkeleton cols={columns.length} />;
  }

  if (data.length === 0) {
    return <EmptyState icon={emptyIcon} title={emptyMessage} />;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-slate-100 text-xs uppercase tracking-wide text-slate-400">
            {columns.map((col) => (
              <th key={col.header} className={clsx("px-5 py-3 font-medium", col.className)}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr
              key={rowKey(row)}
              className="border-b border-slate-50 transition-colors last:border-0 hover:bg-slate-50/80"
            >
              {columns.map((col) => (
                <td key={col.header} className={clsx("px-5 py-3.5 text-slate-700", col.className)}>
                  {col.accessor(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
