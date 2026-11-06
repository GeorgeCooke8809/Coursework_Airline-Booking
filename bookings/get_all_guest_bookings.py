from models.base import with_session
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from models import Guest, Booking, BookingSeat, Guest, Flight
from utils import ExistenceException

from flights import calculate_flight_duration

from datetime import datetime, timedelta, UTC
from pytz import timezone
import logging

LOGGER = logging.getLogger(__name__)

def _bookings_list_to_tuples(session: Session, bookings_list: list[Booking]):
    to_return = []

    for booking in bookings_list:
        flight_duration = calculate_flight_duration(session, booking.flight_id)
        departure_time_utc = booking.flight.scheduled_departure_datetime_utc.replace(tzinfo=UTC)

        to_return.append((
            booking.booking_id,
            booking.flight.service.route.origin.name,
            booking.flight.service.route.origin.iata,
            departure_time_utc.astimezone(timezone(booking.flight.service.route.origin.timezone)),
            booking.flight.service.route.destination.name,
            booking.flight.service.route.destination.iata,
            flight_duration,
            departure_time_utc.astimezone(timezone(booking.flight.service.route.destination.timezone)) + flight_duration,
            len(booking.seats)
        ))

    return to_return

@with_session
def get_all_guest_bookings(session: Session, user_id: int) -> dict:
    """Gets a list of all past and present bookings for the user and returns details. Bookings are ordered by datetime of departure.
    #### Return Format:
    {
        "past": [
                (
                    <booking_id>: int,
                    <departure_airport_name>: str,
                    <departure_airport_iata>: str,
                    <departure_local_datetime>: datetime,
                    <arrival_airport_name>: str,
                    <arrival_airport_iata>: str,
                    <flight_duration>: timedelta,
                    <arrival_local_datetime>,                    
                    <number_of_companions>: int
                )
            ],
        "future": [
                (
                    <booking_id>: int,
                    <departure_airport_name>: str,
                    <departure_airport_iata>: str,
                    <departure_local_datetime>: datetime,
                    <arrival_airport_name>: str,
                    <arrival_airport_iata>: str,
                    <flight_duration>: timedelta,
                    <arrival_local_datetime>: datetime,                    
                    <number_of_companions>: int
                )
            ]
    }

    Args:
        Session (Session): The database session automatically created by @with_session
        user_id (int): The user ID for the query
    """

    LOGGER.info("Getting all guest bookings...")
    LOGGER.debug(f"{user_id = }")

    user = (
        session.query(Guest)
        .filter(Guest.guest_id == user_id)
    ).first()

    if user is None:
        LOGGER.error("User does not exist to get bookings for")
        raise ExistenceException

    past_bookings = (
        session.query(Booking)
        .join(Flight, Booking.flight_id == Flight.flight_id)
        .filter(Booking.guest_id == user_id)
        .filter(or_(Flight.status == "departed", and_(Flight.status == "cancelled", Flight.scheduled_departure_datetime_utc < datetime.now())))
    ).all()

    LOGGER.debug(f"{past_bookings = }")

    future_bookings = (
            session.query(Booking)
            .join(Flight, Booking.flight_id == Flight.flight_id)
            .filter(Booking.guest_id == user_id)
            .filter(or_(Flight.status == "scheduled", and_(Flight.status == "cancelled", Flight.scheduled_departure_datetime_utc >= datetime.now())))
        ).all()

    LOGGER.debug(f"{past_bookings = }")

    return {
        "past": _bookings_list_to_tuples(session, past_bookings),
        "future": _bookings_list_to_tuples(session, future_bookings)
    }