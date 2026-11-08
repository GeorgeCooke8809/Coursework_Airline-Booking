import pytest
from pytest import raises

from users import add_airline_employee, add_guest, add_companion
from bookings import create_unpaid_booking
from flights import create_route, add_one_off_flight
from seats import add_booking_seat, edit_booking_seat

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight, BookingSeat

from utils.exceptions import ExistenceException, SeatException

LOGGER = logging.getLogger(__name__)

def test_edit_booking_seat_new_seat_all_valid(session: Session):
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

    edit_booking_seat(session, 1, new_seat="1B")

    assert session.query(BookingSeat).first().seat_id == "1B"

def test_edit_booking_seat_new_seat_invalid_does_not_exist(session: Session):
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

    with raises(SeatException):
        edit_booking_seat(session, 1, new_seat="1E")

def test_edit_booking_seat_new_seat_invalid_already_booked(session: Session):
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
    add_booking_seat(session, 1, 1, "1B")

    with raises(SeatException):
        edit_booking_seat(session, 1, new_seat="1B")



def test_edit_booking_seat_companion_all_valid(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Companion
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")
    add_companion(session, 1, "Jamie Allsop", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)
    add_booking_seat(session, 1, 1, "1A")

    edit_booking_seat(session, 1, new_companion_id=2)

    assert session.query(BookingSeat).first().companion_id == 2


def test_edit_booking_seat_companion_invalid_does_not_exist(session: Session):
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
        edit_booking_seat(session, 1, new_companion_id=2)

def test_edit_booking_seat_companion_invalid_does_ownership_miss_match(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Companion
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    add_guest(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "07802 447086", "password123*")
    add_companion(session, 2, "Jamie Allsop", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)
    add_booking_seat(session, 1, 1, "1A")

    with raises(SeatException):
        edit_booking_seat(session, 1, new_companion_id=2)