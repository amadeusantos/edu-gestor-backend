from core.infrastructure.database.engine import DatabaseEngine
from core.infrastructure.database.session import db_session, get_session
from core.infrastructure.database.tables import RoleEnum, User
from core.infrastructure.environment.manage import settings
from core.infrastructure.security.password import hash_password


@db_session
def create_super_user(engine: DatabaseEngine, **kwargs) -> None:
    session = get_session(**kwargs)

    if session.query(User).filter_by(email=settings.SUPER_USER_EMAIL).first():
        return

    session.add(
        User(
            email=settings.SUPER_USER_EMAIL,
            password=hash_password(settings.SUPER_USER_PASSWORD),
            role=RoleEnum.ADMIN,
        )
    )
    session.commit()
