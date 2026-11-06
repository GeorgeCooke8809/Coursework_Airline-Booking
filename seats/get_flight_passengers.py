from models.base import with_session
from sqlalchemy.orm import Session

from models import Companion, BookingSeat, Flight, Booking
from utils import ExistenceException

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_flight_passengers(session: Session, flight_id: int) -> list[tuple[int, str, str]]:
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
    LOGGER.info("Getting flight passengers...")
    LOGGER.debug(f"{flight_id = }")

    flight = (
        session.query(Flight)
        .filter(Flight.flight_id == flight_id)
    ).first()

    if flight in None:
        LOGGER.error("Flight does not exist to get passenger list")
        raise ExistenceException

    passengers = (
        session.query(BookingSeat.booking_seat_id, Companion.passport_name, BookingSeat.status)
        .join(Companion, BookingSeat.companion_id == Companion.companion_id)
        .join(Booking, BookingSeat.booking_id == Booking.booking_id)
        .filter(Booking.flight_id == flight_id)
    ).all()

    return [tuple(passenger) for passenger in passengers]