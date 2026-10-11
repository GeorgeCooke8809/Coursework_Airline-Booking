from models.base import with_session
from sqlalchemy.orm import Session

@with_session
def get_all_user_bookings(Session: Session):
    pass