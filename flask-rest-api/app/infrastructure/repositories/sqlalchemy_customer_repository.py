from typing import List, Optional, Tuple

from app.domain.entities.customer import Customer
from app.domain.repositories.customer_repository import CustomerRepository
from app.infrastructure.extensions import db
from app.infrastructure.models import CustomerModel


def _to_entity(model: CustomerModel) -> Customer:
    return Customer(
        id=model.id,
        name=model.name,
        phone=model.phone,
        email=model.email,
        created_at=model.created_at,
    )


class SqlAlchemyCustomerRepository(CustomerRepository):
    def add(self, customer: Customer) -> Customer:
        model = CustomerModel(name=customer.name, phone=customer.phone, email=customer.email)
        db.session.add(model)
        db.session.commit()
        return _to_entity(model)

    def get(self, customer_id: int) -> Optional[Customer]:
        model = db.session.get(CustomerModel, customer_id)
        return _to_entity(model) if model else None

    def list_all(self) -> List[Customer]:
        models = CustomerModel.query.order_by(CustomerModel.id).all()
        return [_to_entity(model) for model in models]

    def list_paginated(
        self, page: int, per_page: int, search: Optional[str] = None
    ) -> Tuple[List[Customer], int]:
        query = CustomerModel.query
        if search:
            query = query.filter(CustomerModel.name.ilike(f"%{search}%"))

        total = query.count()
        models = query.order_by(CustomerModel.id).offset((page - 1) * per_page).limit(per_page).all()
        return [_to_entity(model) for model in models], total

    def update(self, customer: Customer) -> Customer:
        model = db.session.get(CustomerModel, customer.id)
        model.name = customer.name
        model.phone = customer.phone
        model.email = customer.email
        db.session.commit()
        return _to_entity(model)
