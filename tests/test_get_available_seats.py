import pytest
from pytest import raises

from users import add_airline_employee, add_guest, add_companion
from bookings import create_unpaid_booking
from flights import create_route, add_one_off_flight
from seats import get_available_seats, add_booking_seat

from models import VALID_SEAT_IDS

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_get_available_seats_all_valid_all_free(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    assert set(get_available_seats(session, 1)) == set(VALID_SEAT_IDS)

def test_get_available_seats_all_valid_one_taken(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Companion
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)

    # Actual test
    add_booking_seat(session, 1, 1, "1A")

    assert set(get_available_seats(session, 1)) == set(VALID_SEAT_IDS) - set(["1A"])

def test_get_available_seats_invalid_flight_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_available_seats(session, 1)