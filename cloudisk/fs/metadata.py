from datetime import datetime
from pathlib import Path

from sqlalchemy import inspect
from sqlmodel import Field, Session, SQLModel, create_engine, select

from cloudisk import logger
from cloudisk.fs.utils import get_mime_type
from cloudisk.vars import METADATA_PATH


class Metadata(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    file_path: str
    file_size: int = 0
    content_type: str = ""

    available: bool = True

    created_at: int = 0
    updated_at: int = 0
    deleted_at: int = 0

    downloads: int = 0


class MetadataManager:
    def __init__(self):  # noqa: D107
        self.engine = self.get_engine()

    @staticmethod
    def get_engine():
        return create_engine(f"sqlite:///{METADATA_PATH}")

    @property
    def available_paths(self):
        engine = MetadataManager.get_engine()

        if not inspect(engine).has_table(Metadata.__tablename__):
            return []

        with Session(engine) as session:
            statement = select(Metadata.file_path).where(Metadata.available)
            results = session.exec(statement)

            return results.all()

    def create(self, path: Path, file_size: int = 0, content_type: str = ""):
        SQLModel.metadata.create_all(self.engine)

        with Session(self.engine) as session:
            if inspect(self.engine).has_table(Metadata.__tablename__):
                # TODO unavailable paths get overwritten
                paths = self.available_paths

                if path._str in paths:
                    raise ValueError(f"File with name '{path._str}' already exist")

            metadata = Metadata(
                file_path=path._str,
                file_size=file_size or path.stat().st_size,
                content_type=content_type or get_mime_type(path),
            )

            now = int(datetime.now().timestamp())

            metadata.created_at = now
            metadata.updated_at = now

            session.add(metadata)
            session.commit()

    def remove(self, path: Path):
        with Session(self.engine) as session:
            statement = select(Metadata).where(Metadata.file_path == path._str)
            results = session.exec(statement)

            if not (metadata := results.first()):
                logger.error("Error on remove")
                return

            metadata.available = False

            now = int(datetime.now().timestamp())

            metadata.updated_at = now
            metadata.deleted_at = now

            session.add(metadata)
            session.commit()

    def update_downloads(self, path: Path):
        with Session(self.engine) as session:
            statement = select(Metadata).where(Metadata.file_path == path._str)
            results = session.exec(statement)

            if not (metadata := results.first()):
                logger.error("Error on update_downloads")
                return

            metadata.downloads += 1
            metadata.updated_at = int(datetime.now().timestamp())

            session.add(metadata)
            session.commit()
