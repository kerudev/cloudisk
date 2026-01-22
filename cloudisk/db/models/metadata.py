from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel, select

from cloudisk.db.models.base import ModelManager
from cloudisk.fs.utils import get_mime_type
from cloudisk.logger import logger


class MetadataModel(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)

    path: str = Field(unique=True)
    size: int = 0
    content_type: str = ""

    available: bool = True

    created_at: int = 0
    updated_at: int = 0
    deleted_at: int = 0

    downloads: int = 0


class Metadata(ModelManager):
    model = MetadataModel

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

    def create(self, path: Path) -> Optional[MetadataModel]:
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
        """
        SQLModel.metadata.create_all(self.engine)

        path_str = str(path)

        with Session(self.engine) as session:
            now = int(datetime.now().timestamp())

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
                logger.error(f"Path '{path_str}' already exist")
                return None

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
            metadata = self.select_or_create_path(path)
            metadata.available = False

            now = int(datetime.now().timestamp())
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
            metadata.updated_at = int(datetime.now().timestamp())

            session.add(metadata)
            session.commit()
