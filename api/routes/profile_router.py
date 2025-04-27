from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from contracts.requests.user_request import ProfileFiltersRequest, ProfileRequest
from contracts.responses.base import ProblemResponse
from contracts.responses.user_response import ProfileResponse
from core.application.users.profiles.create_profile import (
    create_profile as create_profile_service,
)
from core.application.users.profiles.delete_profile import (
    delete_profile as delete_profile_service,
)
from core.application.users.profiles.get_all_profiles import (
    get_all_profiles as get_all_profiles_service,
)
from core.application.users.profiles.get_profile_by_id import (
    get_profile_by_id as get_profile_by_id_service,
)
from core.application.users.profiles.update_profile import (
    update_profile as update_profile_service,
)
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
    create_profile_request: ProfileRequest,
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
def get_all_profiles(
    filter_query: Annotated[ProfileFiltersRequest, Query()],
    db_session: DbSession,
    response: Response,
    _: Annotated[User, Depends(Authorizer([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))],
) -> list[ProfileResponse]:
    profiles, count = get_all_profiles_service(filter_query, db_session)

    response.headers["X-Total-Count"] = str(count)
    response.headers["X-Page"] = str(filter_query.page)
    response.headers["X-Page-Size"] = str(filter_query.page_size)
    response.headers["X-Total-Pages"] = str(
        (count // filter_query.page_size)
        + (1 if count % filter_query.page_size > 0 else 0)
    )

    return profiles


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
        status.HTTP_403_FORBIDDEN: {"model": ProblemResponse},
        status.HTTP_404_NOT_FOUND: {"model": ProblemResponse},
    },
)
def get_profile_by_id(
    id: str,
    db_session: DbSession,
    _: Annotated[User, Depends(Authorizer([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))],
) -> ProfileResponse:
    return get_profile_by_id_service(id, db_session)


@router.put(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
        status.HTTP_403_FORBIDDEN: {"model": ProblemResponse},
        status.HTTP_404_NOT_FOUND: {"model": ProblemResponse},
    },
)
def update_profile(
    id: str,
    update_profile_request: ProfileRequest,
    db_session: DbSession,
    _: Annotated[User, Depends(Authorizer([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))],
) -> None:
    update_profile_service(id, update_profile_request, db_session)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ProblemResponse},
        status.HTTP_403_FORBIDDEN: {"model": ProblemResponse},
        status.HTTP_404_NOT_FOUND: {"model": ProblemResponse},
    },
)
def delete_profile(
    id: str,
    db_session: DbSession,
    _: Annotated[User, Depends(Authorizer([RoleEnum.ADMIN, RoleEnum.COORDINATOR]))],
) -> None:
    delete_profile_service(id, db_session)
