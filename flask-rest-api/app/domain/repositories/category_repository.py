from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def add(self, category: Category) -> Category: ...

    @abstractmethod
    def get(self, category_id: int) -> Optional[Category]: ...

    @abstractmethod
    def get_by_name(self, name: str, parent_id: Optional[int]) -> Optional[Category]:
        """Find a category by name among siblings sharing the same parent_id."""

    @abstractmethod
    def list_all(self) -> List[Category]: ...

    @abstractmethod
    def list_children(self, parent_id: int) -> List[Category]: ...

    @abstractmethod
    def update(self, category: Category) -> Category: ...

    @abstractmethod
    def delete(self, category_id: int) -> bool: ...
