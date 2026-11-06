import pytest
from pytest import raises

from users import add_airline_employee, add_guest, add_companion, add_airport_staff
from bookings import create_unpaid_booking
from flights import create_route, add_one_off_flight
from seats import add_booking_seat, get_flight_passengers

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight, BookingSeat

from utils.exceptions import ExistenceException, AuthorisationException

LOGGER = logging.getLogger(__name__)

def test_get_flight_passengers_all_valid_multiple(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Companion
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")
    add_companion(session, 1, "Jamie Allsop", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")
    add_companion(session, 1, "Akil Rameez", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)

    add_booking_seat(session, 1, 1, "1A")
    add_booking_seat(session, 1, 2, "1B")
    add_booking_seat(session, 1, 3, "1C")

    assert get_flight_passengers(session, 1, 1) == [(1, "1A","George Arthur Collins Cooke", "not-arrived"), (2, "1B","Jamie Allsop", "not-arrived"), (3, "1C","Akil Rameez", "not-arrived")]

def test_get_flight_passengers_all_valid_empty(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    assert get_flight_passengers(session, 1, 1) == []

def test_get_flight_passengers_invalid_flight_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(ExistenceException):
        get_flight_passengers(session, 1, 1)

def test_get_flight_passengers_invalid_airport_staff_does_not_exist(session: Session):
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

    add_booking_seat(session, 1, 1, "1A")

    with raises(ExistenceException):
        get_flight_passengers(session, 1, 1)

def test_get_flight_passengers_invalid_airport_staff_does_not_have_access(session: Session):
    LOGGER.critical("Expecting error")
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "KJFK")

        # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Companion
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)

    add_booking_seat(session, 1, 1, "1A")

    with raises(AuthorisationException):
        get_flight_passengers(session, 1, 1)