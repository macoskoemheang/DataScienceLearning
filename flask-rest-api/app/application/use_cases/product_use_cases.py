from typing import List, Optional, Tuple

from app.application.exceptions import ConflictError, NotFoundError, ValidationError
from app.domain.entities.product import Product
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.sale_repository import SaleRepository


def _validate_category(category_repository: CategoryRepository, category_id: Optional[int]):
    if category_id is not None and category_repository.get(category_id) is None:
        raise ValidationError(f"category {category_id} does not exist")


class ListProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self) -> List[Product]:
        return self.product_repository.list_all()

    def execute_paginated(
        self,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> Tuple[List[Product], int]:
        page = max(page, 1)
        per_page = min(max(per_page, 1), 100)
        return self.product_repository.list_paginated(page, per_page, search, category_id)


class GetProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int) -> Product:
        product = self.product_repository.get(product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found")
        return product


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository, category_repository: CategoryRepository):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def execute(
        self,
        name: str,
        price,
        sku: str = "",
        stock_quantity: int = 0,
        category_id: Optional[int] = None,
    ) -> Product:
        if not name:
            raise ValidationError("'name' is required")
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValidationError("'price' must be a number")
        if price < 0:
            raise ValidationError("'price' cannot be negative")
        if stock_quantity < 0:
            raise ValidationError("'stock_quantity' cannot be negative")
        _validate_category(self.category_repository, category_id)

        product = Product(
            name=name,
            price=price,
            sku=sku,
            stock_quantity=stock_quantity,
            category_id=category_id,
        )
        return self.product_repository.add(product)


class UpdateProductUseCase:
    def __init__(self, product_repository: ProductRepository, category_repository: CategoryRepository):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def execute(self, product_id: int, **fields) -> Product:
        product = self.product_repository.get(product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found")

        if "name" in fields:
            if not fields["name"]:
                raise ValidationError("'name' cannot be empty")
            product.name = fields["name"]
        if "sku" in fields:
            product.sku = fields["sku"]
        if "price" in fields:
            try:
                price = float(fields["price"])
            except (TypeError, ValueError):
                raise ValidationError("'price' must be a number")
            if price < 0:
                raise ValidationError("'price' cannot be negative")
            product.price = price
        if "stock_quantity" in fields:
            stock_quantity = fields["stock_quantity"]
            if not isinstance(stock_quantity, int) or stock_quantity < 0:
                raise ValidationError("'stock_quantity' must be a non-negative integer")
            product.stock_quantity = stock_quantity
        if "category_id" in fields:
            _validate_category(self.category_repository, fields["category_id"])
            product.category_id = fields["category_id"]

        return self.product_repository.update(product)


class AddStockUseCase:
    """Restock an existing product by adding to its current stock_quantity
    (as opposed to UpdateProductUseCase, which overwrites it directly).
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: int, quantity: int) -> Product:
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError("'quantity' must be a positive integer")

        product = self.product_repository.get(product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found")

        product.stock_quantity += quantity
        return self.product_repository.update(product)


class DeleteProductUseCase:
    def __init__(self, product_repository: ProductRepository, sale_repository: SaleRepository):
        self.product_repository = product_repository
        self.sale_repository = sale_repository

    def execute(self, product_id: int) -> None:
        if self.product_repository.get(product_id) is None:
            raise NotFoundError(f"Product {product_id} not found")
        if self.sale_repository.is_product_referenced(product_id):
            raise ConflictError("cannot delete a product that has existing sales")

        self.product_repository.delete(product_id)
