from fastapi import APIRouter, Query
from pydantic import BaseModel

from cloudisk.db.models.user import User, UserModel

router = APIRouter(prefix="/auth", tags=["auth"])


class UserRegisterForm(BaseModel):
    username: str
    email: str
    password: str


class UserLoginForm(BaseModel):
    # username: str
    email: str
    password: str


@router.post("/register")
async def register(body: UserRegisterForm) -> UserModel:
    """Register route."""
    user = User().register(
        username=body.username,
        email=body.email,
        password=body.password,
    )

    return user


@router.get("/verify")
async def verify(email: str = Query(...)) -> UserModel:
    user = User().verify(email=email)

    return user


@router.post("/login")
async def login(body: UserLoginForm) -> UserModel:
    user = User().login(
        email=body.email,
        password=body.password,
    )

    return user
