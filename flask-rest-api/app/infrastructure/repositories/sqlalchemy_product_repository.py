from typing import List, Optional, Tuple

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.extensions import db
from app.infrastructure.models import ProductModel


def _to_entity(model: ProductModel) -> Product:
    return Product(
        id=model.id,
        name=model.name,
        sku=model.sku,
        price=model.price,
        stock_quantity=model.stock_quantity,
        category_id=model.category_id,
        created_at=model.created_at,
    )


class SqlAlchemyProductRepository(ProductRepository):
    def add(self, product: Product) -> Product:
        model = ProductModel(
            name=product.name,
            sku=product.sku,
            price=product.price,
            stock_quantity=product.stock_quantity,
            category_id=product.category_id,
        )
        db.session.add(model)
        db.session.commit()
        return _to_entity(model)

    def get(self, product_id: int) -> Optional[Product]:
        model = db.session.get(ProductModel, product_id)
        return _to_entity(model) if model else None

    def list_all(self) -> List[Product]:
        models = ProductModel.query.order_by(ProductModel.id).all()
        return [_to_entity(model) for model in models]

    def list_paginated(
        self,
        page: int,
        per_page: int,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> Tuple[List[Product], int]:
        query = ProductModel.query
        if search:
            query = query.filter(ProductModel.name.ilike(f"%{search}%"))
        if category_id is not None:
            query = query.filter(ProductModel.category_id == category_id)

        total = query.count()
        models = query.order_by(ProductModel.id).offset((page - 1) * per_page).limit(per_page).all()
        return [_to_entity(model) for model in models], total

    def update(self, product: Product) -> Product:
        model = db.session.get(ProductModel, product.id)
        model.name = product.name
        model.sku = product.sku
        model.price = product.price
        model.stock_quantity = product.stock_quantity
        model.category_id = product.category_id
        db.session.commit()
        return _to_entity(model)

    def delete(self, product_id: int) -> bool:
        model = db.session.get(ProductModel, product_id)
        if model is None:
            return False
        db.session.delete(model)
        db.session.commit()
        return True
