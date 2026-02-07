from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, select

from cloudisk.db.links import UserGroupLink

from .base import ModelManager

if TYPE_CHECKING:
    from cloudisk.db.models.group import GroupModel

# TODO save encrypted passwords


class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)

    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str

    last_login: Optional[datetime] = Field(None, nullable=True)

    is_verified: bool = False

    groups: list["GroupModel"] = Relationship(
        back_populates="users",
        link_model=UserGroupLink,
    )


class User(ModelManager):
    model = UserModel

    class Error(Exception):
        """Raised when the problem doesn't fit any of the other exceptions."""

    class DoesNotExist(Error):  # noqa: N818
        """Raised when the user doesn't exist in the database."""

    class UsernameExists(Error):  # noqa: N818
        """Raised when the user's `username` is already registered."""

    class EmailExists(Error):  # noqa: N818
        """Raised when the user's `email` is already registered."""

    class NotVerified(Error):  # noqa: N818
        """Raised when the user is not verified."""

    class IncorrectPassword(Error):  # noqa: N818
        """Raised when the user is registered but has provided an incorrect password."""

    def register(self, username: str, email: str, password: str) -> UserModel:
        """
        Register a new user into the database.

        Parameters
        ----------
        username: str
            The user's name or nick.
        email: str
            The user's email.
        password: str
            The user's password.

        Returns
        -------
        UserModel
            The created user.

        Raises
        ------
        User.UsernameExists
            When the user's `username` is already used.
        User.EmailExists
            When the user's `email` is already used.
        """
        with Session(self.engine) as session:
            query_username = select(self.model.username).where(
                self.model.username == username
            )
            if session.exec(query_username).one_or_none():
                raise User.UsernameExists(f"Username '{username}' already exists")

            query_email = select(self.model.email).where(self.model.email == email)
            if session.exec(query_email).one_or_none():
                raise User.EmailExists(f"Email '{email}' already exists")

            user = self.model(
                username=username,
                email=email,
                password=password,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def verify(self, email: str, password: str) -> UserModel:
        """
        Verify a user's account.

        Parameters
        ----------
        email: str
            The user's email.
        password: str
            The user's password.

        Returns
        -------
        UserModel
            The created user.

        Raises
        ------
        User.DoesNotExist
            When the user doesn't exist.
        User.IncorrectPassword
            When the user's `password` is not correct.
        """
        with Session(self.engine) as session:
            if not (user := self.one_or_none(email)):
                raise User.DoesNotExist("User is not registered")

            if user.password != password:
                raise User.IncorrectPassword("Passwords don't match")

            user.is_verified = True

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def login(self, email: str, password: str) -> UserModel:
        """
        Mark a user as logged in.

        Parameters
        ----------
        email: str
            The user's email.
        password: str
            The user's password.

        Returns
        -------
        UserModel
            The created user.

        Raises
        ------
        User.DoesNotExist
            When a user doesn't exist.
        User.NotVerified
            When a user is not verified.
        User.IncorrectPassword
            When the user's `password` is not correct.
        """
        with Session(self.engine) as session:
            if not (user := self.one_or_none(email)):
                raise User.DoesNotExist("User is not registered")

            if not user.is_verified:
                raise User.NotVerified("User is not verified")

            if user.password != password:
                raise User.IncorrectPassword("Passwords don't match")

            user.last_login = datetime.now()

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def one_or_none(self, email: str) -> Optional[UserModel]:
        """
        Return the user with `email`.

        Parameters
        ----------
        email: str
            The user's email.

        Returns
        -------
        Optional[UserModel]
            The matching user or `None`.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.email == email)
            results = session.exec(statement)

            return results.one_or_none()
