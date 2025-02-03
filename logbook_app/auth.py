from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from ninja.security import HttpBearer

from .utils import JWT_ALGORITHM, JWT_EXPIRATION_TIME, JWT_SECRET_KEY


class JWTAuth(HttpBearer):
    async def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(
                jwt=token,
                key=JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
            user_id = payload.get("sub")

            if not user_id:
                return None

            user = await User.objects.aget(id=user_id)
            return user  # This will be available as `request.auth`

        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            ObjectDoesNotExist,
        ):
            return None


async def generate_jwt_token(user: User):
    """Generate a JWT token for the given user."""
    expiration_time = datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_TIME)

    payload = {
        "sub": str(user.pk),
        "username": str(user.username),
        "exp": expiration_time,
    }

    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return token
