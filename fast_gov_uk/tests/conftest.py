from pathlib import Path
from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup
from fasthtml import common as fh

from fast_gov_uk.design_system import AbstractField


@pytest.fixture
def fast():
    from .app import fast
    # Mock notify for testing
    fast.notify_client = Mock()
    return fast


@pytest.fixture
def client(fast):
    return fh.Client(fast)


@pytest.fixture(scope="function")
def db(fast):
    db = fast.db
    db.q("BEGIN TRANSACTION;")
    yield db
    db.q("ROLLBACK;")


@pytest.fixture
def picture():
    this_file = Path(__file__).resolve()
    parent = this_file.parent
    return open(parent / "picture.png", "rb")


@pytest.fixture
def html():
    def pretty_html(x):
        if isinstance(x, AbstractField):
            html_str = fh.to_xml(x)
        elif isinstance(x, fh.FT):
            html_str = str(x)
        else:
            html_str = x
        soup = BeautifulSoup(html_str, "html.parser")
        return soup.prettify()
    return pretty_html
