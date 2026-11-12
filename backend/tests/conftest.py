import pytest
from typing import Generator


@pytest.fixture
def app():
    """Fixture que proporciona la aplicación FastAPI para testing."""
    from app.main import create_app
    return create_app()


@pytest.fixture
def client(app):
    """Fixture que proporciona un cliente HTTP para testing."""
    from httpx import AsyncClient
    from starlette.testclient import TestClient
    return TestClient(app)
