import pytest
from fastapi.testclient import TestClient

from app.api import cars
from app.main import app


@pytest.fixture(autouse=True)
def reset_db():
    # La base est en mémoire : on la restaure après chaque test pour les isoler
    snapshot = [car.model_copy() for car in cars.db_cars]
    yield
    cars.db_cars[:] = snapshot


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
