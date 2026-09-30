from typing import List

from werkzeug.security import check_password_hash, generate_password_hash

from app.application.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.domain.entities.user import ROLE_ADMIN, ROLE_CASHIER, User
from app.domain.repositories.user_repository import UserRepository


class RegisterUserUseCase:
    """Public self-registration. The very first account in the system
    becomes admin (bootstrap); everyone after that is a cashier by default.
    Use CreateEmployeeUseCase (admin-only) to assign roles explicitly.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, password: str) -> User:
        if not username or not password:
            raise ValidationError("'username' and 'password' are required")
        if self.user_repository.get_by_username(username):
            raise ConflictError("username already taken")

        is_first_user = len(self.user_repository.list_all()) == 0
        role = ROLE_ADMIN if is_first_user else ROLE_CASHIER

        user = User(username=username, password_hash=generate_password_hash(password), role=role)
        return self.user_repository.add(user)


class CreateEmployeeUseCase:
    """Admin-only: create a staff account with an explicit role."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, password: str, role: str = ROLE_CASHIER) -> User:
        if not username or not password:
            raise ValidationError("'username' and 'password' are required")
        if role not in (ROLE_ADMIN, ROLE_CASHIER):
            raise ValidationError(f"'role' must be one of: {ROLE_ADMIN}, {ROLE_CASHIER}")
        if self.user_repository.get_by_username(username):
            raise ConflictError("username already taken")

        user = User(username=username, password_hash=generate_password_hash(password), role=role)
        return self.user_repository.add(user)


class AuthenticateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, password: str) -> User:
        user = self.user_repository.get_by_username(username)
        if not user or not check_password_hash(user.password_hash, password or ""):
            raise AuthenticationError("invalid username or password")
        if not user.is_active:
            raise AuthenticationError("this account has been deactivated")
        return user


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("user not found")
        return user


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        return self.user_repository.list_all()


class UpdateEmployeeUseCase:
    """Admin-only: change an employee's role and/or active status.

    Employees are never hard-deleted (they may be referenced by past
    sales) -- deactivating (is_active=False) is how you remove someone's
    access.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int, role: str = None, is_active: bool = None) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("user not found")

        if role is not None:
            if role not in (ROLE_ADMIN, ROLE_CASHIER):
                raise ValidationError(f"'role' must be one of: {ROLE_ADMIN}, {ROLE_CASHIER}")
            user.role = role
        if is_active is not None:
            user.is_active = bool(is_active)

        return self.user_repository.update(user)
