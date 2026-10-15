from models.base import with_session
from sqlalchemy.orm import Session

from models import BookingSeat, Companion, Booking, VALID_SEAT_IDS

@with_session
def edit_booking_seat(Session: Session, booking_seat_id: int, new_seat: str = None, new_companion_id: int = None) -> None:
    """Edits the given booking seat record with the new details. Raises exception if new companion and booking ownership mismatch or if seat is invalid

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_seat_id (int): The booking seat ID to edit
        new_seat (str, optional): The new seat for the companion. Defaults to None.
        new_companion_id (int, optional): The new companion. Defaults to None.
    """