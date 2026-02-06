from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

from .base import ModelManager


class GroupModel(SQLModel, table=True):
    __tablename__ = "groups"

    id: int = Field(primary_key=True)

    name: str = Field(unique=True)


class Group(ModelManager):
    model = GroupModel

    class Error(Exception):
        """Raised when the problem doesn't fit any of the other exceptions."""

    class AlreadyExists(Error):  # noqa: N818
        """Raised when the group already exists."""

    def create(self, name: str) -> GroupModel:
        """
        Create a new user group.

        Parameters
        ----------
        name: str
            The group's name.

        Returns
        -------
        GroupModel
            The created group.

        Raises
        ------
        Group.AlreadyExists
            When the group's `name` is already used.
        """
        with Session(self.engine) as session:
            query = select(self.model.name).where(self.model.name == name)
            if session.exec(query).one_or_none():
                raise Group.AlreadyExists(f"Group '{name}' already exists")

            group = self.model(name=name)

            session.add(group)
            session.commit()
            session.refresh(group)

            return group

    def one_or_none(self, name: str) -> Optional[GroupModel]:
        """
        Return the group with `name`.

        Parameters
        ----------
        name: str
            The group's name.

        Returns
        -------
        Optional[GroupModel]
            The matching group or `None`.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.name == name)
            results = session.exec(statement)

            return results.one_or_none()
