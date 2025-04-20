from datetime import datetime, timedelta, timezone
from typing import Tuple
import jwt
from core.infrastructure.environment.manage import settings


def create_access_token(username: str) -> Tuple[str, float]:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt, expire.timestamp()
