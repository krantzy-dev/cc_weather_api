import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.app import app
from src.config import settings
from src.database import get_db
from src.models import Base
from tests.integration.seed import load_seed_data


@pytest.fixture(scope="session")
def engine():
    """
    Create the test database (if needed) and the schema once per test session.
    """
    admin_url = (
        f"postgresql+psycopg://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/postgres"
    )
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": settings.test_db_name},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{settings.test_db_name}"'))
    admin_engine.dispose()

    test_engine = create_engine(settings.test_db_url)
    Base.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def db_session(engine):
    """
    Provide a session bound to a transaction that is rolled back after the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """
    Provide a TestClient with the real DB dependency swapped for the test session.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_db(db_session):
    """
    Like db_session, but pre-populated with the shared seed dataset.
    """
    load_seed_data(db_session)
    return db_session


@pytest.fixture
def seeded_client(seeded_db):
    """
    Like client, but backed by a pre-populated database.
    """

    def override_get_db():
        yield seeded_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
