from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    name: str
    phone: str = ""
    email: str = ""
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
