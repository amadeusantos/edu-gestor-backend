from uuid import UUID

from sqlalchemy.orm import Session

from api.user.exceptions import UserEmailAlreadyExistsException
from api.user.schemas import UserCreateSchema, UserUpdateSchema
from infrastructure.persistence.models import UserModel


def validate_create_user(session: Session, user_create: UserCreateSchema):
    user = session.query(UserModel).where(UserModel.email == user_create.email).first()

    if user:
        raise UserEmailAlreadyExistsException()


def validate_update_user(session: Session, user_create: UserUpdateSchema, user_id: UUID):
    user = (
        session.query(UserModel)
            .where(UserModel.email == user_create.email, UserModel.id != user_id)
        .first()
    )

    if user:
        raise UserEmailAlreadyExistsException()
