from datetime import datetime
from typing import List, Optional, Tuple

from app.application.exceptions import NotFoundError, ValidationError
from app.domain.entities.sale import Sale, SaleItem
from app.domain.repositories.customer_repository import CustomerRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository


class CreateSaleUseCase:
    """Checkout: validates stock, snapshots unit prices, and persists the
    sale together with the resulting stock decrements as one atomic write.
    """

    def __init__(
        self,
        sale_repository: SaleRepository,
        product_repository: ProductRepository,
        customer_repository: CustomerRepository,
    ):
        self.sale_repository = sale_repository
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def execute(self, employee_id: int, items: list, customer_id: Optional[int] = None) -> Sale:
        if not items:
            raise ValidationError("at least one item is required")
        if customer_id is not None and self.customer_repository.get(customer_id) is None:
            raise NotFoundError(f"Customer {customer_id} not found")

        sale_items = []
        stock_updates = {}

        for entry in items:
            product_id = entry.get("product_id")
            quantity = entry.get("quantity")

            if not isinstance(product_id, int) or not isinstance(quantity, int) or quantity <= 0:
                raise ValidationError("each item needs an integer 'product_id' and a positive integer 'quantity'")

            product = self.product_repository.get(product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} not found")

            remaining = stock_updates.get(product.id, product.stock_quantity)
            if remaining < quantity:
                raise ValidationError(f"insufficient stock for product '{product.name}'")

            sale_items.append(
                SaleItem(product_id=product.id, quantity=quantity, unit_price=product.price)
            )
            stock_updates[product.id] = remaining - quantity

        sale = Sale(employee_id=employee_id, customer_id=customer_id, items=sale_items)
        return self.sale_repository.create_sale(sale, stock_updates)


class GetSaleUseCase:
    def __init__(self, sale_repository: SaleRepository):
        self.sale_repository = sale_repository

    def execute(self, sale_id: int) -> Sale:
        sale = self.sale_repository.get(sale_id)
        if sale is None:
            raise NotFoundError(f"Sale {sale_id} not found")
        return sale


class ListSalesUseCase:
    def __init__(self, sale_repository: SaleRepository):
        self.sale_repository = sale_repository

    def execute(self) -> List[Sale]:
        return self.sale_repository.list_all()

    def execute_paginated(
        self,
        page: int = 1,
        per_page: int = 20,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Tuple[List[Sale], int]:
        page = max(page, 1)
        per_page = min(max(per_page, 1), 100)
        return self.sale_repository.list_paginated(page, per_page, start_date, end_date)
