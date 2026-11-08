from models.base import with_session
from sqlalchemy.orm import Session

from models import BookingSeat, Companion
from utils import ExistenceException, SeatException
from .get_available_seats import get_available_seats

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def edit_booking_seat(session: Session, booking_seat_id: int, new_seat: str = None, new_companion_id: int = None) -> None:
    """Edits the given booking seat record with the new details. Raises exception if new companion and booking ownership mismatch or if seat is invalid

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_seat_id (int): The booking seat ID to edit
        new_seat (str, optional): The new seat for the companion. Defaults to None.
        new_companion_id (int, optional): The new companion. Defaults to None.
    """
    LOGGER.info("Editing booking seat...")
    LOGGER.debug(f"{booking_seat_id = }, {new_seat = }, {new_companion_id = }")

    booking_seat = (
        session.query(BookingSeat)
        .filter(BookingSeat.booking_seat_id == booking_seat_id)
    ).first()

    if booking_seat is None:
        LOGGER.error("Booking seat does not exist")
        raise ExistenceException

    if new_seat is not None:
        if new_seat not in get_available_seats(session, booking_seat.booking.flight_id):
            LOGGER.error("Seat does not exist or is already booked")
            raise SeatException

        booking_seat.seat_id = new_seat

    if new_companion_id is not None:
        new_companion = (
            session.query(Companion)
            .filter(Companion.companion_id == new_companion_id)
        ).first()

        if new_companion is None:
            LOGGER.error("Given companion does not exist")
            raise ExistenceException

        if new_companion.guest_id != booking_seat.booking.guest_id:
            LOGGER.error("Companion and booking ownership miss match")
            raise SeatException

        booking_seat.companion = new_companion