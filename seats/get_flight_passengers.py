from models.base import with_session
from sqlalchemy.orm import Session

from models import Companion, BookingSeat, Flight, Booking

@with_session
def get_flight_passengers(Session: Session, flight_id: int) -> list[tuple[int, str, str]]:
    """Gets and returns a list of all the passengers booked on to a flight. Used in the gate and check in agent portals.

    ## Return Format:
        [
            (
                <booking_seat_id>: int,
                <companion_passport_name>: str,
                <passenger_status>: str
            )
        ]

    Args:
        Session (Session): The database session automatically provided by @with_session
        flight_id (int): The flight ID to get passengers for
    """