from sqlalchemy.orm import Session
from contracts.responses.user_response import ProfileResponse
from core.infrastructure.database.tables import Profile
from core.infrastructure.database.utils import get_by_attribute


def get_profile_by_id(profile_id: str, db_session: Session) -> ProfileResponse:
    profile = get_by_attribute(
        session=db_session,
        model=Profile,
        attribute_name="id",
        attribute_value=profile_id,
    )

    return ProfileResponse.from_row(profile)
