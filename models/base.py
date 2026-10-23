from pathlib import Path

from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import create_engine, event

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "data" / "data.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def with_session(func: function):
    """With session wrapper designed to auto create and pass session into functions that require it. Allows for passing existing session if given for unit tests.

    Args:
        func (function): The function for the session to be passed into
    """

    # TODO: Allow for passing session in manually and not creating a new session when done. Optional

    def wrap(*args, **kwargs):
        session = SessionLocal()

        if args and isinstance(args[0], Session) or isinstance(kwargs.get("session"), Session):
            result = func(*args, **kwargs)
            return result
        else:
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