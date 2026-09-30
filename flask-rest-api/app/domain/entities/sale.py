from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class SaleItem:
    product_id: int
    quantity: int
    unit_price: float
    id: Optional[int] = None

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal,
        }


@dataclass
class Sale:
    employee_id: int
    items: List[SaleItem] = field(default_factory=list)
    customer_id: Optional[int] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    @property
    def total_amount(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "customer_id": self.customer_id,
            "items": [item.to_dict() for item in self.items],
            "total_amount": self.total_amount,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
