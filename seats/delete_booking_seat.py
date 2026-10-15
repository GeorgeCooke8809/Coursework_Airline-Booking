from models.base import with_session
from sqlalchemy.orm import Session

from models import BookingSeat

@with_session
def delete_booking_seat(Session: Session, booking_seat_id: int) -> None:
    """Deletes the given BookingSeat record

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_seat_id (int): The ID of the booking seat record to be delete
    """