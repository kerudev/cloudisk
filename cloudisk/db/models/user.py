from datetime import datetime
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, select

from .base import ModelManager

# TODO save encrypted passwords


class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(primary_key=True)

    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str

    last_login: Optional[datetime] = Field(None, nullable=True)

    is_verified: bool = False


class User(ModelManager):
    model = UserModel

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
        Exception
            When a user is already registered.
        """
        with Session(self.engine) as session:
            user = self.model(
                username=username,
                email=email,
                password=password,
            )

            session.add(user)

            try:
                session.commit()
            except IntegrityError:
                raise Exception(f"User '{email}' already exist")

            session.refresh(user)

            return user

    def verify(self, email: str) -> UserModel:
        """
        Verify a user's account.

        Parameters
        ----------
        email: str
            The user's email.

        Returns
        -------
        UserModel
            The created user.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.email == email)
            results = session.exec(statement)

            user = results.one()
            user.is_verified = True

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def login(self, email: str) -> UserModel:
        """
        Mark a user as logged in.

        Parameters
        ----------
        email: str
            The user's email.

        Returns
        -------
        UserModel
            The created user.

        Raises
        ------
        Exception
            - When a user doesn't exist.
            - When a user is not verified.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.email == email)
            results = session.exec(statement)

            user = results.one_or_none()

            if not user:
                raise Exception("User is not registered")

            if not user.is_verified:
                raise Exception("User is not verified")

            user.last_login = datetime.now()

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def exists(self, email: str) -> bool:
        """
        Check if a user exists.

        Parameters
        ----------
        email: str
            The user's email.

        Returns
        -------
        bool
            `True` if a user exists. `False` otherwise.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.email == email)
            results = session.exec(statement)

            user = results.one_or_none()

            return bool(user)
