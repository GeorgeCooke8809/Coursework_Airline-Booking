from models.base import with_session
from sqlalchemy.orm import Session

from models import Companion, BookingSeat, Flight, Booking, AirportStaff
from utils import ExistenceException, AuthorisationException

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_flight_passengers(Session: Session, flight_id: int, airport_staff_id: int) -> list[tuple[int, str, str]]:
    """Gets and returns a list of all the passengers booked on to a flight. Used in the gate and check in agent portals.

    ## Return Format:
        [
            (
                <booking_seat_id>: int,
                <seat_id>: str,
                <companion_passport_name>: str,
                <passenger_status>: str
            )
        ]

    Args:
        Session (Session): The database session automatically provided by @with_session
        flight_id (int): The flight ID to get passengers for
        airport_staff_id (int): The ID of the staff member requesting information to confirm they have access
    """
    LOGGER.info("Getting flight passengers...")
    LOGGER.debug(f"{flight_id = }")

    flight = (
        session.query(Flight)
        .filter(Flight.flight_id == flight_id)
    ).first()

    if flight is None:
        LOGGER.error("Flight does not exist to get passenger list")
        raise ExistenceException

    airport_staff = (
        session.query(AirportStaff)
        .filter(AirportStaff.airport_staff_id == airport_staff_id)
    ).first()

    if airport_staff is None:
        LOGGER.error("Airport staff member does not exist")
        raise ExistenceException

    if airport_staff.assigned_airport_icao != flight.service.route.origin_icao:
        LOGGER.error("The airport staff member does not have permission to view the given flight")
        raise AuthorisationException

    passengers = (
        session.query(BookingSeat.booking_seat_id, BookingSeat.seat_id, Companion.passport_name, BookingSeat.status)
        .join(Companion, BookingSeat.companion_id == Companion.companion_id)
        .join(Booking, BookingSeat.booking_id == Booking.booking_id)
        .filter(Booking.flight_id == flight_id)
        .order_by(BookingSeat.seat_id)
    ).all()

    return [tuple(passenger) for passenger in passengers]