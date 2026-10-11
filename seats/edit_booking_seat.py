from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def edit_booking_seat(Session: Session):
    pass