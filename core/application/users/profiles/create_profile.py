from sqlalchemy.orm import Session
from contracts.requests.user_request import CreateProfileRequest
from contracts.responses.user_response import ProfileResponse
from core.infrastructure.database.utils import create


def create_profile(
    profile_request: CreateProfileRequest, db_session: Session
) -> ProfileResponse:
    created_profile = create(db_session, profile_request.to_row())

    return ProfileResponse.from_row(created_profile)
