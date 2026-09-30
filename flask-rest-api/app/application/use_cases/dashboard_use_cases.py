from app.domain.repositories.customer_repository import CustomerRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository


class GetDashboardSummaryUseCase:
    def __init__(
        self,
        sale_repository: SaleRepository,
        product_repository: ProductRepository,
        customer_repository: CustomerRepository,
    ):
        self.sale_repository = sale_repository
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def execute(self, low_stock_threshold: int = 5) -> dict:
        sales = self.sale_repository.list_all()
        products = self.product_repository.list_all()
        customers = self.customer_repository.list_all()

        total_revenue = round(sum(sale.total_amount for sale in sales), 2)
        low_stock_count = sum(1 for p in products if p.stock_quantity <= low_stock_threshold)

        return {
            "total_revenue": total_revenue,
            "total_sales": len(sales),
            "total_products": len(products),
            "total_customers": len(customers),
            "low_stock_count": low_stock_count,
        }


class TopProductsUseCase:
    def __init__(self, sale_repository: SaleRepository, product_repository: ProductRepository):
        self.sale_repository = sale_repository
        self.product_repository = product_repository

    def execute(self, limit: int = 5) -> list:
        sales = self.sale_repository.list_all()

        quantity_by_product = {}
        revenue_by_product = {}
        for sale in sales:
            for item in sale.items:
                quantity_by_product[item.product_id] = (
                    quantity_by_product.get(item.product_id, 0) + item.quantity
                )
                revenue_by_product[item.product_id] = (
                    revenue_by_product.get(item.product_id, 0) + item.subtotal
                )

        ranked = sorted(quantity_by_product.items(), key=lambda kv: kv[1], reverse=True)[:limit]

        result = []
        for product_id, quantity_sold in ranked:
            product = self.product_repository.get(product_id)
            if product is None:
                continue
            result.append(
                {
                    "product": product.to_dict(),
                    "quantity_sold": quantity_sold,
                    "revenue": round(revenue_by_product[product_id], 2),
                }
            )
        return result


class LowStockProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, threshold: int = 5) -> list:
        products = self.product_repository.list_all()
        return [p for p in products if p.stock_quantity <= threshold]


class RecentSalesUseCase:
    def __init__(self, sale_repository: SaleRepository):
        self.sale_repository = sale_repository

    def execute(self, limit: int = 10) -> list:
        sales, _ = self.sale_repository.list_paginated(page=1, per_page=limit)
        return sales
