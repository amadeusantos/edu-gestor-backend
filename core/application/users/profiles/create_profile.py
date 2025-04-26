from sqlalchemy.orm import Session
from contracts.requests.user_request import CreateProfileRequest
from contracts.responses.user_response import ProfileResponse


def create_profile(
    profile_request: CreateProfileRequest, db_session: Session
) -> ProfileResponse:
    profile = profile_request.to_row()
    db_session.add(profile)
    db_session.flush()

    return ProfileResponse.from_row(profile)
