from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from app.domain.entities.customer import Customer


class CustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer) -> Customer: ...

    @abstractmethod
    def get(self, customer_id: int) -> Optional[Customer]: ...

    @abstractmethod
    def list_all(self) -> List[Customer]: ...

    @abstractmethod
    def list_paginated(
        self, page: int, per_page: int, search: Optional[str] = None
    ) -> Tuple[List[Customer], int]:
        """Return (items, total_matching_count)."""

    @abstractmethod
    def update(self, customer: Customer) -> Customer: ...
