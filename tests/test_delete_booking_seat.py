import pytest
from pytest import raises

from users import add_airline_employee, add_guest, add_companion
from bookings import create_unpaid_booking
from flights import create_route, add_one_off_flight, change_flight_status
from seats import add_booking_seat, delete_booking_seat

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight, BookingSeat

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_delete_booking_seat_all_valid(session: Session):
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

    delete_booking_seat(session, 1)

    assert session.query(BookingSeat).count() == 0

def test_delete_booking_seat_invalid_booking_seat_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        delete_booking_seat(session, 1)

def test_delete_booking_seat_invalid_flight_already_departed(session: Session):
    LOGGER.critical("Expecting error")

    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Companion
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)

    change_flight_status(session, 1, "departed")

    # Actual test
    add_booking_seat(session, 1, 1, "1A")

    with raises(InvalidDateException):
        delete_booking_seat(session, 1)