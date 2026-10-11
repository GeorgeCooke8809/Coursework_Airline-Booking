from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def get_flight_passengers(Session: Session):
    pass