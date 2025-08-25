import pytest
from starlette.testclient import TestClient

from fast_gov_uk import core


@pytest.fixture
def dev_client():
    settings = {"DATABASE_URL": ":memory:", "DEV_MODE": True}
    app = core.Fast(settings)
    return TestClient(app)


def test_demo(dev_client):
    response = dev_client.get("/demo")
    assert response.status_code == 200
