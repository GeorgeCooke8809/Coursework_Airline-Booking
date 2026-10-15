from models.base import with_session
from sqlalchemy.orm import Session

from models import Booking, Companion, BookingSeat, Flight, VALID_SEAT_IDS

@with_session
def add_booking_seat(Session: Session, booking_id: int, companion_id: int, seat_id: str) -> None:
    """Creates a new booking seat entry with the given details. Raises an exception if companion and booking ownership mismatch, seat is already taken for flight, or if seat_id is invalid. Status is defaulted as not arrived.

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_id (int): The booking ID to attach the record to
        companion_id (int): The companion to attach the record to
        seat_id (str): The seat that the companion will be taking
    """