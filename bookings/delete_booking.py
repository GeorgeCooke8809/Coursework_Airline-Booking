from models.base import with_session
from sqlalchemy.orm import Session

from models import Booking, BookingSeat
from utils import ExistenceException, InvalidDateException

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def delete_booking(session: Session, booking_id: int) -> None:
    """Deletes the given booking from the booking_id as well as any booking_Seats assigned to it. Raises InvalidDateException if the flight has already departed.

    Args:
        session (Session): The database session automatically provided by the with_session wrapper
        booking_id (int): The primary key identifier of the booking to be deleted
    """
    LOGGER.info("Deleting booking")
    LOGGER.debug(f"{booking_id = }")

    booking = (
        session.query(Booking)
        .filter(Booking.booking_id == booking_id)
    ).first()

    if booking is None:
        LOGGER.error("Booking does not exist to delete")
        raise ExistenceException

    if booking.flight.status == "departed":
        LOGGER.error("Flight has already departed so cannot delete a booking on it.")
        raise InvalidDateException

    session.query(BookingSeat).filter(BookingSeat.booking_id == booking_id).delete()
    session.delete(booking)