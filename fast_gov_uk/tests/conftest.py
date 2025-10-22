from pathlib import Path
from unittest.mock import Mock

import pytest
from bs4 import BeautifulSoup
from fasthtml import common as fh
from starlette.testclient import TestClient

from fast_gov_uk.design_system import AbstractField
from fast_gov_uk.forms import Form


@pytest.fixture
def fast():
    from .app import fast
    # Mock notify for testing
    fast.notify_client = Mock()
    return fast


@pytest.fixture
def client(fast):
    return fh.Client(fast)


@pytest.fixture
def error_client(fast):
    return TestClient(fast, raise_server_exceptions=False)


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
        elif isinstance(x, Form):
            html_str = fh.to_xml(x)
        elif isinstance(x, fh.FT):
            html_str = str(x)
        else:
            html_str = str(x)
        soup = BeautifulSoup(html_str, "html.parser")
        return soup.prettify()
    return pretty_html


@pytest.fixture
def find():
    def _find(html, tag, selector):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find(tag, selector)
    return _find
