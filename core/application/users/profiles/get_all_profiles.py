from sqlalchemy.orm import Session
from contracts.requests.user_request import ProfileFiltersRequest
from contracts.responses.user_response import ProfileResponse
from core.infrastructure.database.tables import Profile
from core.infrastructure.database.utils import get_all


def get_all_profiles(
    filters_request: ProfileFiltersRequest,
    db_session: Session,
):
    profiles, total = get_all(
        session=db_session,
        model=Profile,
        page=filters_request.page,
        page_size=filters_request.page_size,
        filters=filters_request.to_query_filters(),
    )

    return [ProfileResponse.from_row(profile) for profile in profiles], total
