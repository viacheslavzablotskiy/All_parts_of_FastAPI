import pytest
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker, Session
from starlette.testclient import TestClient

from src.db.database import get_db, engine
from src.main import app
from src.db.database import metadata
from src.db.config import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST

DATABASE_URL_TEST = f"postgresql://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"


engine_test = create_engine(DATABASE_URL_TEST, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)
metadata.bind = engine_test



def override_get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
def prepare_database():
    with engine_test.begin() as conn:
        conn.run_sync(metadata.create_all)
    yield
    with engine_test.begin() as conn:
        conn.run_sync(metadata.drop_all)


client = TestClient(app)
