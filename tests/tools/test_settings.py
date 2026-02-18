import os
from types import ModuleType

import pytest

from cloudisk.tools.settings import Settings
from cloudisk.vars import CLOUDISK_ROOT
from tests.conftest import TEST_MAIL

CONFTEST_MODULE = "tests.conftest"


def test__init__env():
    instance = Settings()

    assert instance.module is None


def test__init__module():
    instance = Settings(CONFTEST_MODULE)

    assert isinstance(instance.module, ModuleType)


def test_get_env():
    instance = Settings()

    instance.set_default(FOO="test")

    assert instance.get("FOO") == "test"
    assert instance.get("FOO") == instance.FOO

    assert instance.get("BAR", "foo") == "foo"
    assert instance.BAR is None


def test_get_module():
    instance = Settings(CONFTEST_MODULE)

    instance.set_default(FOO="test")

    assert instance.get("FOO") == "test"
    assert instance.get("FOO") == instance.FOO

    assert instance.get("BAR", "baz") == "baz"
    assert instance.BAR is None

    assert instance.TEST_MAIL == TEST_MAIL


def test_set_default_env():
    instance = Settings()

    instance.set_default(FOO="test", BAR=CLOUDISK_ROOT, TEST_MAIL="another@mail.com")

    assert instance.FOO == os.environ["CLOUDISK_FOO"] == "test"
    assert instance.BAR == os.environ["CLOUDISK_BAR"] == str(CLOUDISK_ROOT)
    assert instance.TEST_MAIL == "another@mail.com"


def test_set_default_module():
    instance = Settings(CONFTEST_MODULE)

    instance.set_default(FOO="test", BAR=CLOUDISK_ROOT, TEST_MAIL="another@mail.com")

    assert instance.FOO == instance.module.FOO == "test"
    assert instance.BAR == instance.module.BAR == CLOUDISK_ROOT
    assert instance.TEST_MAIL == TEST_MAIL


def test_clear_cache():
    instance = Settings()

    instance.set_default(FOO="test")
    instance.get("FOO")
    instance.get("FOO")

    instance.clear_cache()

    assert instance.get.cache_info().hits == 0


def test_check_key_ok():
    assert Settings()._check_key("KEY") is None


def test_check_key_raises_BadKeyFormat_wrong_type():
    with pytest.raises(Settings.BadKeyFormat):
        Settings()._check_key(123)


def test_check_key_raises_BadKeyFormat_not_uppercase():
    with pytest.raises(Settings.BadKeyFormat):
        Settings()._check_key("key")
