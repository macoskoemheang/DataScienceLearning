from typing import List, Optional

from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.extensions import db
from app.infrastructure.models import CategoryModel


def _to_entity(model: CategoryModel) -> Category:
    return Category(id=model.id, name=model.name, parent_id=model.parent_id)


class SqlAlchemyCategoryRepository(CategoryRepository):
    def add(self, category: Category) -> Category:
        model = CategoryModel(name=category.name, parent_id=category.parent_id)
        db.session.add(model)
        db.session.commit()
        return _to_entity(model)

    def get(self, category_id: int) -> Optional[Category]:
        model = db.session.get(CategoryModel, category_id)
        return _to_entity(model) if model else None

    def get_by_name(self, name: str, parent_id: Optional[int]) -> Optional[Category]:
        model = CategoryModel.query.filter_by(name=name, parent_id=parent_id).first()
        return _to_entity(model) if model else None

    def list_all(self) -> List[Category]:
        models = CategoryModel.query.order_by(CategoryModel.id).all()
        return [_to_entity(model) for model in models]

    def list_children(self, parent_id: int) -> List[Category]:
        models = CategoryModel.query.filter_by(parent_id=parent_id).order_by(CategoryModel.id).all()
        return [_to_entity(model) for model in models]

    def update(self, category: Category) -> Category:
        model = db.session.get(CategoryModel, category.id)
        model.name = category.name
        model.parent_id = category.parent_id
        db.session.commit()
        return _to_entity(model)

    def delete(self, category_id: int) -> bool:
        model = db.session.get(CategoryModel, category_id)
        if model is None:
            return False
        db.session.delete(model)
        db.session.commit()
        return True
