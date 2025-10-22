import pytest  # type: ignore
from app import app as flask_app


@pytest.fixture
def app():
    """Esta fixture proporciona tu app de Flask a pytest-flask."""
    yield flask_app


def test_home_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Docker" in resp.get_data(as_text=True)
