from models.base import with_session
from sqlalchemy.orm import Session

from models import Booking
from utils import ExistenceException

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def pay_booking(Session: Session, booking_id: int) -> None:
    """Mark the given booking as paid for.

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_id (int): The booking ID to mark as paid
    """

    LOGGER.info("Marking booking as paid...")
    LOGGER.debug(f"{booking_id  =}")

    booking = (
        Session.query(Booking)
        .filter(Booking.booking_id == booking_id)
    ).first()

    if booking is None:
        LOGGER.error("Booking does not exist to update")
        raise ExistenceException

    booking.payment_cleared = True