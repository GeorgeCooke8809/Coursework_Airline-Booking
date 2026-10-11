from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def delete_booking_seat(Session: Session):
    pass