from models.base import with_session
from sqlalchemy.orm import Session

from models import BookingSeat, VALID_PASSENGER_STATUS
from utils import ExistenceException, CompanionException

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def change_booking_seat_status(session: Session, booking_Seat_id: int, new_status: str) -> None:
    """Changes the booking seat status. Used when marking passengers as checked-in or boarded

    Args:
        session (Session): The database session automatically given by the with_session wrapper
        booking_Seat_id (int): The ID of the booking seat record to update
        new_status (str): "not-arrived" | "checked" | "boarded" : The new status of the seat
    """
    LOGGER.info("Updating booking seat status...")
    LOGGER.debug(f"{booking_Seat_id = }, {new_status = }")

    booking_seat = (
        session.query(BookingSeat)
        .filter(BookingSeat.booking_seat_id == booking_Seat_id)
    ).first()

    if booking_seat is None:
        LOGGER.error("Booking seat does not exist to update")
        raise ExistenceException

    if new_status not in VALID_PASSENGER_STATUS:
        LOGGER.error(f"New status is not in valid options {VALID_PASSENGER_STATUS = }")
        raise CompanionException