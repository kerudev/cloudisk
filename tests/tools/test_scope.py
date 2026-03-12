import pytest
from sqlmodel import Session

from cloudisk.db.models.space import Space
from cloudisk.tools.scope import Scope
from cloudisk.vars import CLOUDISK_SETTINGS_FILE


def test__init__(fake_db):
    instance = Scope("test", engine_path=fake_db)

    assert instance.name == "test"
    assert instance.engine_path == fake_db
    assert instance.settings_path is None
    assert instance.settings_module is None

    assert instance.extras == {}
    assert instance._engine is None
    assert instance._settings is None


def test_engine(fake_db):
    instance = Scope("test", engine_path=fake_db)

    assert str(instance.engine.url) == f"sqlite:///{fake_db}"
    assert instance._engine is not None


def test_settings(tmp_path, fake_db):
    fake_settings_path = tmp_path / CLOUDISK_SETTINGS_FILE
    fake_settings_path.touch()

    instance = Scope(
        "test",
        engine_path=fake_db,
        settings_path=fake_settings_path,
    )

    assert instance.settings.path == fake_settings_path
    assert instance.settings.module is not None


def test_set_engine(fake_db):
    instance = Scope("test", engine_path=fake_db)

    instance.set_engine()

    assert instance._engine is not None


def test_set_engine_uses_previously_created(fake_db):
    instance = Scope("test", engine_path=fake_db)

    instance.set_engine(path=fake_db)
    assert instance._engine is not None


def test_update_space(fake_db):
    manager = Space()
    manager.create(name="foo")
    manager.use(name="foo")

    instance = Scope("test", engine_path=fake_db)
    instance.update_space()

    assert instance.extras["space_id"] == 1
    assert instance.extras["space_name"] == "foo"


def test_update_space_no_space_table(fake_db):
    instance = Scope("test", engine_path=fake_db)

    with pytest.raises(Scope.NoSpace):
        instance.update_space()


def test_update_space_no_space_used(fake_db):
    manager = Space()
    space = manager.create(name="foo")

    with Session(manager.engine) as session:
        space.used = False

        session.add(space)
        session.commit()

    instance = Scope("test", engine_path=fake_db)

    with pytest.raises(Scope.NoSpace):
        instance.update_space()


def test_cleanup(fake_db):
    instance = Scope("test", engine_path=fake_db)

    instance.set_engine()
    instance.cleanup()

    assert instance._engine is None


def test_create_engine(fake_db):
    instance = Scope("test", engine_path=fake_db)

    engine = instance._create_engine()

    assert str(engine.url) == f"sqlite:///{fake_db}"
