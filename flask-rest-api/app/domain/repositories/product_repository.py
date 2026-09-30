from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from app.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product) -> Product: ...

    @abstractmethod
    def get(self, product_id: int) -> Optional[Product]: ...

    @abstractmethod
    def list_all(self) -> List[Product]: ...

    @abstractmethod
    def list_paginated(
        self,
        page: int,
        per_page: int,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> Tuple[List[Product], int]:
        """Return (items, total_matching_count)."""

    @abstractmethod
    def update(self, product: Product) -> Product: ...

    @abstractmethod
    def delete(self, product_id: int) -> bool: ...
