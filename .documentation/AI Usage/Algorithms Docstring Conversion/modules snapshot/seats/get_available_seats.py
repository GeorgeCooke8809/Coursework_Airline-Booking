from models.base import with_session
from sqlalchemy.orm import Session

from models import BookingSeat, Flight, VALID_SEAT_IDS

@with_session
def get_available_seats(Session: Session, flight_id: int) -> list:
    """gets and returns a list of all the seat IDs that are still available on the given flight.

    Args:
        Session (Session): The database session automatically provided by @with_session
        flight_id (int): The flight to check the seat availability of.
    """