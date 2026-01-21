from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import Engine, create_engine, inspect
from sqlmodel import SQLModel

from cloudisk.vars import CLOUDISK_DB_PATH

T = TypeVar("T", bound=SQLModel)


class AbstractManager(ABC):
    @abstractmethod
    def table_exists(self) -> bool:
        """
        Check if the table exists in the database.

        Returns
        -------
        bool
            `True` if the table exists. `False` otherwise.
        """

    # @abstractmethod
    # def one():
    #     ...

    # @abstractmethod
    # def all():
    #     ...

    # @abstractmethod
    # def create():
    #     ...

    # @abstractmethod
    # def where():
    #     ...


class ModelManager(AbstractManager, Generic[T]):
    def __init__(self, model: T) -> None:  # noqa: D107
        self.model = model
        self.engine = self.get_engine()

    # Abstract

    def table_exists(self) -> bool:
        return inspect(self.engine).has_table(self.model.__tablename__)

    # Public

    @staticmethod
    def get_engine() -> Engine:
        """
        Create an SQLite `Engine`.

        Returns
        -------
        Engine
            The engine used to run operations on the SQLite database.
        """
        return create_engine(f"sqlite:///{CLOUDISK_DB_PATH}")
