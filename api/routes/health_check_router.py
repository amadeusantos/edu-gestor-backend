from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from contracts.responses.base import ProblemResponse

router = APIRouter()


@router.get(
    "",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ProblemResponse},
    },
)
def health_check(request: Request) -> None:
    if not hasattr(request.state, "db") or not request.state.db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database session is not available",
        )
