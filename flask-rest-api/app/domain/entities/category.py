from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    name: str
    parent_id: Optional[int] = None
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "parent_id": self.parent_id}
