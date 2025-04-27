from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from contracts.requests.user_request import CreateProfileRequest, ProfileFiltersRequest
from contracts.responses.base import ProblemResponse
from contracts.responses.user_response import ProfileResponse
from core.application.users.profiles.create_profile import (
    create_profile as create_profile_service,
)
from core.application.users.profiles.get_all_profiles import get_all_profiles
from core.infrastructure.database.manage import DbSession
from core.infrastructure.database.tables import RoleEnum, User
from core.infrastructure.security.authorizer import Authorizer

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProfileResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
        status.HTTP_403_FORBIDDEN: {"model": ProblemResponse},
        status.HTTP_409_CONFLICT: {"model": ProblemResponse},
    },
)
def create_profile(
    create_profile_request: CreateProfileRequest,
    db_session: DbSession,
    _: Annotated[User, Depends(Authorizer([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))],
) -> ProfileResponse:
    return create_profile_service(create_profile_request, db_session)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ProfileResponse],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
        status.HTTP_403_FORBIDDEN: {"model": ProblemResponse},
    },
)
def get_profiles(
    filter_query: Annotated[ProfileFiltersRequest, Query()],
    db_session: DbSession,
    response: Response,
    _: Annotated[User, Depends(Authorizer([RoleEnum.ADMIN]))],
) -> list[ProfileResponse]:
    profiles, count = get_all_profiles(filter_query, db_session)

    response.headers["X-Total-Count"] = str(count)
    response.headers["X-Page"] = str(filter_query.page)
    response.headers["X-Page-Size"] = str(filter_query.page_size)
    response.headers["X-Total-Pages"] = str(
        (count // filter_query.page_size)
        + (1 if count % filter_query.page_size > 0 else 0)
    )

    return profiles
