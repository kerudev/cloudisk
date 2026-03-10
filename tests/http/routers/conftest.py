import pytest


@pytest.fixture(autouse=True)
def setup(monkeypatch, fake_context):
    monkeypatch.setattr("cloudisk.fs.utils.context", fake_context)
