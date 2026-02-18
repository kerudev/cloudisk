from sqlite3 import IntegrityError

from sqlmodel import Field, Session, SQLModel

from cloudisk.db.models.base import ModelManager


class SpaceModel(SQLModel, table=True):
    __tablename__ = "space"

    id: int = Field(primary_key=True)

    name: str
    protect: bool


class Space(ModelManager):
    model = SpaceModel

    class Error(Exception):
        """Raised when the problem doesn't fit any of the other exceptions."""

    class AlreadyExists(Error):  # noqa: N818
        """Raised when the space already exists."""

    def create(self, name: str, protect: bool) -> SpaceModel:
        """
        Create a `MetadataModel` instance.

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
            When a path is already registered.
        """
        with Session(self.engine) as session:
            space = self.model(
                name=name,
                protect=protect,
            )

            session.add(space)

            try:
                session.commit()
            except IntegrityError:
                raise Space.AlreadyExists(f"Space '{name}' already exist")

            session.refresh(space)

            return space
