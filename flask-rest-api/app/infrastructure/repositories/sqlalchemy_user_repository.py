from typing import List, Optional

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.extensions import db
from app.infrastructure.models import UserModel


def _to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        password_hash=model.password_hash,
        role=model.role,
        is_active=model.is_active,
        created_at=model.created_at,
    )


class SqlAlchemyUserRepository(UserRepository):
    def add(self, user: User) -> User:
        model = UserModel(
            username=user.username,
            password_hash=user.password_hash,
            role=user.role,
            is_active=user.is_active,
        )
        db.session.add(model)
        db.session.commit()
        return _to_entity(model)

    def get_by_id(self, user_id: int) -> Optional[User]:
        model = db.session.get(UserModel, user_id)
        return _to_entity(model) if model else None

    def get_by_username(self, username: str) -> Optional[User]:
        model = UserModel.query.filter_by(username=username).first()
        return _to_entity(model) if model else None

    def list_all(self) -> List[User]:
        models = UserModel.query.order_by(UserModel.id).all()
        return [_to_entity(model) for model in models]

    def update(self, user: User) -> User:
        model = db.session.get(UserModel, user.id)
        model.role = user.role
        model.is_active = user.is_active
        db.session.commit()
        return _to_entity(model)
