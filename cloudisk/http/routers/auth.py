from fastapi import APIRouter
from pydantic import BaseModel

from cloudisk.db.models.user import User, UserModel

router = APIRouter(prefix="/auth", tags=["auth"])


class UserForm(BaseModel):
    username: str
    email: str
    password: str


@router.post("/register")
async def register(body: UserForm) -> UserModel:
    """Register route."""
    user = User().register(
        username=body.username,
        email=body.email,
        password=body.password,
    )

    return user


@router.post("/verify")
async def verify(body: UserForm) -> UserModel:
    user = User().verify(
        email=body.email,
        password=body.password,
    )

    return user


@router.post("/login")
async def login(body: UserForm) -> UserModel:
    user = User().login(
        email=body.email,
        password=body.password,
    )

    return user
