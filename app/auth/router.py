from fastapi import APIRouter, Body, HTTPException, status

from .schema import Token, UserLogin
from .service import authenticate_user, create_access_token

auth_router = APIRouter(prefix="", tags=["Auth"])


@auth_router.post("/token", tags=["Auth"], response_model=Token)
async def create_token(user: UserLogin = Body(...)):
    """
    Create a jwt token for the given user login.
    """
    valid_user = authenticate_user(user)
    if not valid_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_access_token(user.email), "token_type": "bearer"}
