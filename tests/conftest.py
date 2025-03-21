import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from src.persistent_sensor_storage.database import engine, reset_database
from src.persistent_sensor_storage.main import app
from src.persistent_sensor_storage.dependencies import get_db

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db():
    # Reset database to clean state before each test
    reset_database()

    # Create a new session for the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    
    # Remove the override after the test
    app.dependency_overrides.clear()
