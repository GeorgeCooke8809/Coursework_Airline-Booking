from models.base import with_session
from sqlalchemy.orm import Session

from models import BookingSeat, Booking
from utils import ExistenceException, InvalidDateException

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def delete_booking_seat(Session: Session, booking_seat_id: int) -> None:
    """Deletes the given BookingSeat record

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_seat_id (int): The ID of the booking seat record to be delete
    """
    LOGGER.info("Deleting booking seat...")
    LOGGER.debug(f"{booking_seat_id = }")

    booking_seat = (
        Session.query(BookingSeat)
        .filter(BookingSeat.booking_seat_id == booking_seat_id)
    ).first()

    if booking_seat is None:
        LOGGER.error("Booking seat does not exist to delete")
        raise ExistenceException

    if booking_seat.booking.flight.status == "departed":
        LOGGER.error("Cannot delete booking seat when the aircraft has already departed")
        raise InvalidDateException

    Session.delete(booking_seat)