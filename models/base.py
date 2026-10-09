from pathlib import Path

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, event

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "data" / "fs_career.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

Session = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def with_session(func: function):
    """With session wrapper designed to auto create and pass session into functions that require it.

    Args:
        func (function): The function for the session to be passed into
    """
    def wrap(*args, **kwargs):
        session = Session()

        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except:
            session.rollback()
            raise
        finally:
            session.close()
    return wrap