from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

"""
Pytest fixture for testing database in memory only, (heavily) inspired by https://www.youtube.com/watch?v=-Vl7006_CnI
"""



REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "data" / "test_data.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Session = sessionmaker(bind=(engine))

@pytest.fixture(scope="function")
def session():
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()