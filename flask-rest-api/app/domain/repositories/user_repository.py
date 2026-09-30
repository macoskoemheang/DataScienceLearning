from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.user import User


class UserRepository(ABC):
    """Port defining how the application talks to user storage."""

    @abstractmethod
    def add(self, user: User) -> User: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: ...

    @abstractmethod
    def list_all(self) -> List[User]: ...

    @abstractmethod
    def update(self, user: User) -> User: ...
