from models.base import with_session
from sqlalchemy.orm import Session
from models import Booking, BookingSeat

@with_session
def batch_clear_unpaid_bookings(Session: Session) -> None:
    """A regularly run service to delete booking records that have been abandoned (marked as unpaid) > 7 days.

    Args:
        Session (Session): The database session provided automatically with @with_session
    """
    # ? Could add first run prompt user to continue booking