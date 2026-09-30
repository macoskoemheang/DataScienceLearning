from dataclasses import dataclass
from datetime import datetime
from typing import Optional

ROLE_ADMIN = "admin"
ROLE_CASHIER = "cashier"


@dataclass
class User:
    username: str
    password_hash: str
    role: str = ROLE_CASHIER
    is_active: bool = True
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
