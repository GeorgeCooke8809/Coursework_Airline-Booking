from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def generate_boarding_pass(Session: Session):
    pass