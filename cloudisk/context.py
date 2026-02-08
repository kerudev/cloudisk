from sqlalchemy import create_engine

from cloudisk.vars import CLOUDISK_DB_PATH


class Context:
    def __init__(self):  # noqa: D107
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = self._create_engine()

        return self._engine

    def _create_engine(self):
        return create_engine(f"sqlite:///{CLOUDISK_DB_PATH}")


global_context = Context()
