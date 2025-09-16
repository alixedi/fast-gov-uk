from pathlib import Path

import pytest
from bs4 import BeautifulSoup
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


@pytest.fixture
def html():
    def pretty_html(component):
        html_str = str(component)
        soup = BeautifulSoup(html_str, "html.parser")
        return soup.prettify()
    return pretty_html
