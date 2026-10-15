from models.base import with_session
from sqlalchemy.orm import Session

from models import Booking

@with_session
def pay_booking(Session: Session, booking_id: int) -> None:
    """Mark the given booking as paid for.

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_id (int): The booking ID to mark as paid
    """