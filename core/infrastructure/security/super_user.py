from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from core.infrastructure.database.manage import engine
from core.infrastructure.database.tables import Profile, RoleEnum, User
from core.infrastructure.environment.manage import settings
from core.infrastructure.security.password import hash_password


def create_super_user() -> None:
    session = scoped_session(sessionmaker(bind=engine))

    if session.query(User).filter_by(email=settings.SUPER_USER_EMAIL).first():
        session.close()
        session.remove()
        return

    profile = Profile(
        cpf=settings.SUPER_USER_CPF,
        enrollment=None,
        phone=settings.SUPER_USER_PHONE,
        fullname=settings.SUPER_USER_FULLNAME,
        sex=None,
        date_of_birth=datetime.now(),
        father_name=None,
        mother_name=None,
        responsible=None,
        role=RoleEnum.ADMIN,
    )
    session.add(profile)
    session.flush()

    session.add(
        User(
            email=settings.SUPER_USER_EMAIL,
            password=hash_password(settings.SUPER_USER_PASSWORD),
            enabled=True,
            profile_id=profile.id,
        )
    )
    session.commit()

    session.close()
    session.remove()
