from datetime import datetime, timedelta

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app import config

from .schema import UserLogin


def create_access_token(user_email: str) -> str:
    """
    Create a JWT token with the given data and the given expiration time.
    Args:
        user_email: login user email

    Returns:
        JWT token
    """
    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    to_encode: dict = {"sub": user_email}
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    expire = datetime.utcnow() + timedelta(minutes=config.JWT_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    to_encode["iat"] = datetime.utcnow()
    return jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")
            try:
                jwt.decode(credentials.credentials, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
            except (JWTError, ExpiredSignatureError):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


def authenticate_user(data: UserLogin) -> bool:
    """
    Authenticate user with email and password.
    Returns True if user credentials match the stored credentials, False otherwise.

    Args:
        data: UserLogin object containing user's email and password.

    Returns:
        bool: Authentication result.
    """
    return config.APP_EMAIL == data.email and config.APP_PASSWORD == data.password
