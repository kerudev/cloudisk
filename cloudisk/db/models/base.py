from abc import ABC, abstractmethod

from sqlalchemy import inspect
from sqlmodel import Field, SQLModel

from cloudisk.globals import context


class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    space_id: int = Field(default=None, index=True)


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


class ModelManager(AbstractManager):
    def __init__(self):  # noqa: D107
        self.scope = getattr(self.__class__, "scope", context.root)
        self.model = getattr(self.__class__, "model", None)

        self.engine = getattr(self.scope, "engine", None)

        SQLModel.metadata.create_all(self.engine)

    # Abstract

    def table_exists(self) -> bool:
        return inspect(self.engine).has_table(self.model.__tablename__)
