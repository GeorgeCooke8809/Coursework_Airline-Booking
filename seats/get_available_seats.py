from models.base import with_session
from sqlalchemy.orm import Session

from models import BookingSeat, Flight, VALID_SEAT_IDS

from datetime import datetime
import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_available_seats(Session: Session, flight_id: int) -> list:
    """gets and returns a list of all the seat IDs that are still available on the given flight.

    Args:
        Session (Session): The database session automatically provided by @with_session
        flight_id (int): The flight to check the seat availability of.
    """
    flight  =(
        Session.query(Flight)
        .filter(Flight.scheduled_departure_datetime_utc > datetime.now())
        .filter(Flight.flight_id == flight_id)
    ).first()

    if flight is None:
        LOGGER.error("Flight does not exist or has already departed")

    booking_ids = [booking.booking_id for booking in flight.bookings]

    booked_seats = (
        Session.query(BookingSeat)
        .filter(BookingSeat.booking.in_(booking_ids))
    ).all()

    booked_seats = [booking_seat.seat_id for booking_seat in booked_seats]

    available = list(set(VALID_SEAT_IDS) - set(booked_seats))

    return available