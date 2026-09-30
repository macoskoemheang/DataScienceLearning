from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.domain.entities.sale import Sale


class SaleRepository(ABC):
    @abstractmethod
    def create_sale(self, sale: Sale, stock_updates: Dict[int, int]) -> Sale:
        """Persist ``sale`` with its items and apply ``stock_updates``
        (product_id -> new stock_quantity) as a single atomic operation."""

    @abstractmethod
    def get(self, sale_id: int) -> Optional[Sale]: ...

    @abstractmethod
    def list_all(self) -> List[Sale]: ...

    @abstractmethod
    def list_paginated(
        self,
        page: int,
        per_page: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Tuple[List[Sale], int]:
        """Return (items, total_matching_count)."""

    @abstractmethod
    def is_product_referenced(self, product_id: int) -> bool: ...
