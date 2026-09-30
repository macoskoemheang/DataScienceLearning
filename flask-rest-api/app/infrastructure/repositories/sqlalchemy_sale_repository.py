from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.domain.entities.sale import Sale, SaleItem
from app.domain.repositories.sale_repository import SaleRepository
from app.infrastructure.extensions import db
from app.infrastructure.models import ProductModel, SaleItemModel, SaleModel


def _to_entity(model: SaleModel) -> Sale:
    return Sale(
        id=model.id,
        employee_id=model.employee_id,
        customer_id=model.customer_id,
        created_at=model.created_at,
        items=[
            SaleItem(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in model.items
        ],
    )


class SqlAlchemySaleRepository(SaleRepository):
    def create_sale(self, sale: Sale, stock_updates: Dict[int, int]) -> Sale:
        model = SaleModel(employee_id=sale.employee_id, customer_id=sale.customer_id)
        model.items = [
            SaleItemModel(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in sale.items
        ]
        db.session.add(model)

        for product_id, new_quantity in stock_updates.items():
            product_model = db.session.get(ProductModel, product_id)
            product_model.stock_quantity = new_quantity

        db.session.commit()
        return _to_entity(model)

    def get(self, sale_id: int) -> Optional[Sale]:
        model = db.session.get(SaleModel, sale_id)
        return _to_entity(model) if model else None

    def list_all(self) -> List[Sale]:
        models = SaleModel.query.order_by(SaleModel.id).all()
        return [_to_entity(model) for model in models]

    def list_paginated(
        self,
        page: int,
        per_page: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Tuple[List[Sale], int]:
        query = SaleModel.query
        if start_date is not None:
            query = query.filter(SaleModel.created_at >= start_date)
        if end_date is not None:
            query = query.filter(SaleModel.created_at <= end_date)

        total = query.count()
        models = (
            query.order_by(SaleModel.id.desc()).offset((page - 1) * per_page).limit(per_page).all()
        )
        return [_to_entity(model) for model in models], total

    def is_product_referenced(self, product_id: int) -> bool:
        return (
            db.session.query(SaleItemModel.id).filter_by(product_id=product_id).first()
            is not None
        )
