from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def add_booking_seat(Session: Session):
    pass