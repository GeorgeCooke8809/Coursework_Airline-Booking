from models.base import with_session
from sqlalchemy.orm import Session

from models import Booking, Companion, BookingSeat, Flight, VALID_SEAT_IDS
from utils import ExistenceException, SeatException

from .get_available_seats import get_available_seats

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def add_booking_seat(Session: Session, booking_id: int, companion_id: int, seat_id: str) -> None:
    """Creates a new booking seat entry with the given details. Raises an exception if companion and booking ownership mismatch, seat is already taken for flight, or if seat_id is invalid. Status is defaulted as not arrived.

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_id (int): The booking ID to attach the record to
        companion_id (int): The companion to attach the record to
        seat_id (str): The seat that the companion will be taking
    """

    booking = (
        Session.query(Booking)
        .filter(Booking.booking_id == booking_id)
    ).first()

    if booking is None:
        LOGGER.error("Booking does not exist to assign seat to")
        raise ExistenceException

    companion = (
        Session.query(Companion)
        .filter(Companion.companion_id == companion_id)
    ).first()

    if companion is None:
        LOGGER.error("Companion does not exist to assign seat to")
        raise ExistenceException

    if companion.guest_id != booking.guest_id:
        LOGGER.error("Booking and companion ownership don't match")
        raise SeatException

    if seat_id not in get_available_seats(Session, booking.flight_id):
        LOGGER.error("Seat does not exist or is already booked")
        raise SeatException

    new_seat = BookingSeat(booking_id=booking_id, companion_id=companion_id, seat_id=seat_id, status="not-arrived")

    Session.add(new_seat)