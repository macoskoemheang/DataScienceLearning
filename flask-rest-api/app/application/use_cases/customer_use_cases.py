from typing import List, Optional, Tuple

from app.application.exceptions import NotFoundError, ValidationError
from app.domain.entities.customer import Customer
from app.domain.repositories.customer_repository import CustomerRepository


class ListCustomersUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def execute(self) -> List[Customer]:
        return self.customer_repository.list_all()

    def execute_paginated(
        self, page: int = 1, per_page: int = 20, search: Optional[str] = None
    ) -> Tuple[List[Customer], int]:
        page = max(page, 1)
        per_page = min(max(per_page, 1), 100)
        return self.customer_repository.list_paginated(page, per_page, search)


class GetCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def execute(self, customer_id: int) -> Customer:
        customer = self.customer_repository.get(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} not found")
        return customer


class CreateCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def execute(self, name: str, phone: str = "", email: str = "") -> Customer:
        if not name:
            raise ValidationError("'name' is required")
        return self.customer_repository.add(Customer(name=name, phone=phone, email=email))


class UpdateCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    def execute(self, customer_id: int, **fields) -> Customer:
        customer = self.customer_repository.get(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} not found")

        if "name" in fields:
            if not fields["name"]:
                raise ValidationError("'name' cannot be empty")
            customer.name = fields["name"]
        if "phone" in fields:
            customer.phone = fields["phone"]
        if "email" in fields:
            customer.email = fields["email"]

        return self.customer_repository.update(customer)
