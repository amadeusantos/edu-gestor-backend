from contracts.requests.user_request import ProfileRequest
from core.infrastructure.database.manage import DbSession
from core.infrastructure.database.tables import Profile
from core.infrastructure.database.utils import update


def update_profile(
    profile_id: str, update_profile_request: ProfileRequest, db_session: DbSession
) -> None:
    update(
        session=db_session,
        model=Profile,
        id=profile_id,
        **update_profile_request.__dict__
    )
