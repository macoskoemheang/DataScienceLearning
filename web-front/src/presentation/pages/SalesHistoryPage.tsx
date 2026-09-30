import { useState } from "react";
import { Receipt } from "lucide-react";
import { useSales } from "../../application/hooks/useSales";
import { Card } from "../components/ui/Card";
import { Table, type Column } from "../components/ui/Table";
import { Pagination } from "../components/ui/Pagination";
import { Input } from "../components/ui/Input";
import { formatCurrency, formatDate } from "../../lib/formatters";
import type { Sale } from "../../domain/types";

const PER_PAGE = 10;

export function SalesHistoryPage() {
  const [page, setPage] = useState(1);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const { data, isLoading } = useSales({
    page,
    per_page: PER_PAGE,
    start_date: startDate || undefined,
    end_date: endDate || undefined,
  });

  const columns: Column<Sale>[] = [
    { header: "Sale #", accessor: (s) => <span className="font-medium text-slate-800">#{s.id}</span> },
    { header: "Date", accessor: (s) => formatDate(s.created_at) },
    { header: "Items", accessor: (s) => `${s.items.length} item(s)` },
    {
      header: "Total",
      accessor: (s) => <span className="font-semibold text-slate-900">{formatCurrency(s.total_amount)}</span>,
      className: "text-right",
    },
  ];

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-end gap-3">
        <Input
          label="From"
          type="date"
          value={startDate}
          onChange={(e) => {
            setStartDate(e.target.value);
            setPage(1);
          }}
        />
        <Input
          label="To"
          type="date"
          value={endDate}
          onChange={(e) => {
            setEndDate(e.target.value);
            setPage(1);
          }}
        />
      </div>

      <Card>
        <Table
          columns={columns}
          data={data?.items ?? []}
          rowKey={(s) => s.id}
          loading={isLoading}
          emptyIcon={Receipt}
          emptyMessage="No sales in this date range"
        />
        {data && !isLoading && (
          <Pagination page={page} perPage={PER_PAGE} total={data.total} onPageChange={setPage} />
        )}
      </Card>
    </div>
  );
}
