from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, select

from cloudisk.db.models.base import ModelManager
from cloudisk.fs.utils import get_mime_type


class MetadataModel(SQLModel, table=True):
    __tablename__ = "metadata"

    id: int = Field(primary_key=True)

    path: str = Field(unique=True)
    size: int = 0
    content_type: Optional[str] = None

    available: bool = True

    created_at: Optional[datetime] = Field(None, nullable=True)
    updated_at: Optional[datetime] = Field(None, nullable=True)
    deleted_at: Optional[datetime] = Field(None, nullable=True)

    downloads: int = 0


class Metadata(ModelManager):
    model = MetadataModel

    class Error(BaseException):
        """Raised when the problem doesn't fit any of the other exceptions."""

    class PathExists(Error):  # noqa: N818
        """Raised when the user doesn't exist in the database."""

    @property
    def available_paths(self) -> list[str]:
        """
        Return the rows where `available` is `True`.

        Returns
        -------
        list[str]
            Paths where `available` is `True`.
        """
        if not self.table_exists():
            # TODO create metadata objects for each file inside root
            return []

        with Session(self.engine) as session:
            statement = select(self.model.path).where(self.model.available)
            results = session.exec(statement)

            return results.all()

    def select(self, path: Path) -> MetadataModel:
        """
        Select the row where `self.model.path` equals `path`.

        Returns
        -------
        MetadataModel
            The selected instance.
        """
        with Session(self.engine) as session:
            statement = select(self.model).where(self.model.path == str(path))
            results = session.exec(statement)

            return results.first()

    def create(self, path: Path) -> MetadataModel:
        """
        Create a `MetadataModel` instance.

        Parameters
        ----------
        path: Path
            The path to update.

        Returns
        -------
        MetadataModel
            The created instance.

        Raises
        ------
        Metadata.PathExists
            When a path is already registered.
        """
        path_str = str(path)

        with Session(self.engine) as session:
            now = datetime.now()

            metadata = self.model(
                path=path_str,
                size=path.stat().st_size,
                content_type=get_mime_type(path),
                created_at=now,
                updated_at=now,
            )

            session.add(metadata)

            try:
                session.commit()
            except IntegrityError:
                raise Metadata.PathExists(f"Path '{path_str}' already exist")

            session.refresh(metadata)

            return metadata

    def select_or_create_path(self, path: Path) -> MetadataModel:
        """
        Return a `MetadataModel` instance or create it if it doesn't exist.

        Parameters
        ----------
        path: Path
            Path to select or create.

        Returns
        -------
        MetadataModel
            The selected or created path.
        """
        return self.select(path) or self.create(path)

    def remove(self, path: Path) -> None:
        """
        Mark `available` as `False`, but doesn't delete the row, then updates
        the `updated_at` and `deleted_at` with the current timestamp.

        Parameters
        ----------
        path: Path
            The path to update.
        """
        with Session(self.engine) as session:
            now = datetime.now()

            metadata = self.select_or_create_path(path)
            metadata.available = False
            metadata.updated_at = now
            metadata.deleted_at = now

            session.add(metadata)
            session.commit()

    def increment_downloads(self, path: Path) -> None:
        """
        Increments `downloads` by 1, then updates the `updated_at` with the
        current timestamp.

        Parameters
        ----------
        path: Path
            The path to update.
        """
        with Session(self.engine) as session:
            metadata = self.select_or_create_path(path)
            metadata.downloads += 1
            metadata.updated_at = datetime.now()

            session.add(metadata)
            session.commit()
