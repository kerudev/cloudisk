from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, select
from sqlmodel import Field, Session, SQLModel, select

from cloudisk.db.models.base import ModelManager


class SpaceModel(SQLModel, table=True):
    __tablename__ = "space"

    id: int = Field(primary_key=True)

    name: str = Field(unique=True)
    used: bool = False
    protect: bool = False


class Space(ModelManager):
    model = SpaceModel

    class Error(Exception):
        """Raised when the problem doesn't fit any of the other exceptions."""

    class AlreadyExists(Error):  # noqa: N818
        """Raised when the space already exists."""

    def create(self, name: str, protect: bool) -> SpaceModel:
        """
        Create a `SpaceModel` instance.

        Parameters
        ----------
        name: str
            Name of the space.
        protect: bool
            Marks the space as protected with user login.

        Returns
        -------
        SpaceModel
            The created instance.

        Raises
        ------
        Space.AlreadyExists
            When a space already exists.
        """
        with Session(self.engine) as session:
            is_used = self.scope.extras.get("space_id") is None

            space = self.model(name=name, protect=protect, used=is_used)

            session.add(space)

            try:
                session.commit()
            except IntegrityError:
                raise Space.AlreadyExists(f"Space '{name}' already exist")

            session.refresh(space)

            return space

    def remove(self, name: str) -> None:
        """
        Remove a `SpaceModel` from the database.

        Parameters
        ----------
        name: str
            Name of the space.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.name == name)
            results = session.exec(statement)
            space = results.one()

            session.delete(space)
            session.commit()

    def use(self, name: str) -> SpaceModel:
        """
        Set `space.used` to `True`.

        Parameters
        ----------
        name: str
            Name of the space.

        Returns
        -------
        SpaceModel
            The modified instance.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.used == 1)
            results = session.exec(statement)
            space = results.one_or_none()

            if space:
                if space.name == name:
                    return space

                space.used = False

                session.add(space)
                session.commit()

            statement = select(self.model).where(self.model.name == name)
            results = session.exec(statement)
            space = results.one_or_none()

            space.used = True

            session.add(space)
            session.commit()

            return space

    def used(self) -> SpaceModel:
        """
        Get the space where `space.used` is `True`.

        Returns
        -------
        SpaceModel
            The created instance.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.used == 1)
            results = session.exec(statement)
            space = results.one_or_none()

            return space

    def list(self) -> list[str]:
        """
        List all instances of `SpaceModel`.

        Returns
        -------
        list[str]
            The names of the instances.
        """
        with Session(self.engine) as session:
            statement = select(self.model.name)
            results = session.exec(statement)

            return results.all()
