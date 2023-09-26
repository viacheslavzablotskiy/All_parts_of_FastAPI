from sqlalchemy import create_engine, MetaData

from sqlalchemy.orm import sessionmaker
from src.db.config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER

SQL_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

metadata = MetaData()


engine = create_engine(
    SQL_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
