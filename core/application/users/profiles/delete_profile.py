from sqlalchemy.orm import Session
from core.infrastructure.database.tables import Profile
from core.infrastructure.database.utils import delete


def delete_profile(profile_id: str, db_session: Session) -> None:
    delete(session=db_session, model=Profile, id=profile_id)
