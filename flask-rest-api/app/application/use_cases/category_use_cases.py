from typing import List, Optional

from app.application.exceptions import ConflictError, NotFoundError, ValidationError
from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.repositories.product_repository import ProductRepository


def _validate_parent(category_repository: CategoryRepository, parent_id: Optional[int], self_id: Optional[int] = None):
    if parent_id is None:
        return
    if parent_id == self_id:
        raise ValidationError("a category cannot be its own parent")

    parent = category_repository.get(parent_id)
    if parent is None:
        raise NotFoundError(f"Category {parent_id} not found")
    if parent.parent_id is not None:
        raise ValidationError("only one level of subcategories is supported (a subcategory cannot have its own subcategories)")


class ListCategoriesUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self) -> List[Category]:
        return self.category_repository.list_all()


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, name: str, parent_id: Optional[int] = None) -> Category:
        if not name:
            raise ValidationError("'name' is required")
        _validate_parent(self.category_repository, parent_id)

        if self.category_repository.get_by_name(name, parent_id):
            raise ConflictError("a category with this name already exists at this level")

        return self.category_repository.add(Category(name=name, parent_id=parent_id))


class UpdateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, category_id: int, **fields) -> Category:
        category = self.category_repository.get(category_id)
        if category is None:
            raise NotFoundError(f"Category {category_id} not found")

        new_parent_id = category.parent_id
        if "parent_id" in fields:
            new_parent_id = fields["parent_id"]
            _validate_parent(self.category_repository, new_parent_id, self_id=category_id)
            if self.category_repository.list_children(category_id) and new_parent_id is not None:
                raise ValidationError("a category with subcategories cannot itself become a subcategory")

        new_name = category.name
        if "name" in fields:
            if not fields["name"]:
                raise ValidationError("'name' cannot be empty")
            new_name = fields["name"]

        existing = self.category_repository.get_by_name(new_name, new_parent_id)
        if existing and existing.id != category_id:
            raise ConflictError("a category with this name already exists at this level")

        category.name = new_name
        category.parent_id = new_parent_id
        return self.category_repository.update(category)


class DeleteCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository, product_repository: ProductRepository):
        self.category_repository = category_repository
        self.product_repository = product_repository

    def execute(self, category_id: int) -> None:
        if self.category_repository.get(category_id) is None:
            raise NotFoundError(f"Category {category_id} not found")

        if self.category_repository.list_children(category_id):
            raise ConflictError("cannot delete a category that still has subcategories")

        products, _ = self.product_repository.list_paginated(page=1, per_page=1, category_id=category_id)
        if products:
            raise ConflictError("cannot delete a category that still has products assigned to it")

        self.category_repository.delete(category_id)
