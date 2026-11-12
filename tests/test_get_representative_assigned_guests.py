import pytest
from pytest import raises

from users import add_guest, add_airline_employee, get_representative_assigned_guests, add_companion
from flights import create_route, add_one_off_flight
from bookings import create_unpaid_booking
from seats import add_booking_seat

from sqlalchemy.orm import Session
import logging
from datetime import datetime, date, time, timedelta, UTC

from utils import ExistenceException

from models import Guest, AirlineEmployee

LOGGER = logging.getLogger(__name__)

def test_get_representative_assigned_guests_all_valid_one_no_flights(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_representative_assigned_guests(session, 1) == [(
        1,
        "George",
        "Cooke",
        None
    )]

def test_get_representative_assigned_guests_all_valid_multiple_no_flights(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_guest(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "07802 447086", "password123*")

    guests = get_representative_assigned_guests(session, 1)

    assert guests == [
        (
            2,
            "Jamie",
            "Allsop",
            None
        ),
        (
            1,
            "George",
            "Cooke",
            None
        )
    ]

def test_get_representative_assigned_guests_all_valid_one_with_flight(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    create_unpaid_booking(session, 1, 1)
    add_booking_seat(session, 1, 1, "1A")

    assert get_representative_assigned_guests(session, 1) == [(
        1,
        "George",
        "Cooke",
        date.today() + timedelta(days=1)
    )]


def test_get_representative_assigned_guests_no_guests(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    assert get_representative_assigned_guests(session, 1) == []

def test_get_representative_assigned_guests_no_employees(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_representative_assigned_guests(session, 1)

def test_get_representative_assigned_guests_no_representative(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "admin")

    with raises(ExistenceException):
        get_representative_assigned_guests(session, 1)