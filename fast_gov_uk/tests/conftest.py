from pathlib import Path

import pytest
from fasthtml import common as fh


@pytest.fixture
def fast():
    from .app import fast
    return fast


@pytest.fixture
def client(fast):
    return fh.Client(fast)


@pytest.fixture
def db(fast):
    return fast.db


@pytest.fixture
def picture():
    this_file = Path(__file__).resolve()
    parent = this_file.parent
    return open(parent / "picture.png", "rb")
