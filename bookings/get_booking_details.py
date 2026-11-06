from models.base import with_session
from sqlalchemy.orm import Session

from models import Booking, Companion, Flight, BookingSeat
from utils import ExistenceException
from flights import calculate_flight_duration

from datetime import datetime, timedelta, date
import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_booking_details(session: Session, booking_id: int) -> dict:
    """Gets and returns all of the details for thw given booking.

    ## Return Format:
        {
            "departureDatetime": <flight_departure_time>: datetime,
            "flightDuration": <flight_duration>: timedelta,
            "companions": [
                (
                    <companion_passport_name>: str,
                    <companion_date_of_birth>: date,
                    <seat_id>: str,
                    <booking_seat_id>: str
                )
            ]
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_id (int): The booking ID to get details from
    """

    LOGGER.info("Getting booking details...")
    LOGGER.debug(f"{booking_id = }")

    booking = (
        session.query(Booking)
        .filter(Booking.booking_id == booking_id)
    ).first()

    if booking is None:
        LOGGER.error("Booking does not exist to get details for")
        raise ExistenceException

    companions = []

    for seat in booking.seats:
        companions.append((
            seat.companion.passport_name,
            seat.companion.date_of_birth,
            seat.seat_id,
            seat.booking_seat_id
        ))

    return {
        "departureDateTime": booking.flight.scheduled_departure_datetime_utc,
        "flightDuration": calculate_flight_duration(session, booking.flight.flight_id),
        "companions": companions
    }