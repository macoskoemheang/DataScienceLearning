from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    name: str
    price: float
    sku: str = ""
    category_id: Optional[int] = None
    stock_quantity: int = 0
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
