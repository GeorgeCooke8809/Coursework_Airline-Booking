import pytest
from pytest import raises

from users import add_airline_employee, add_guest, add_companion
from bookings import create_unpaid_booking, get_booking_details
from flights import create_route, add_one_off_flight
from seats import add_booking_seat

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight, BookingSeat

from utils.exceptions import ExistenceException, SeatException

LOGGER = logging.getLogger(__name__)

def test_get_booking_details_all_valid(session: Session):
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

    # Actual test
    add_booking_seat(session, 1, 1, "1A")
    add_booking_seat(session, 1, 2, "1B")
    add_booking_seat(session, 1, 3, "1C")

    booking_details = get_booking_details(session, 1)

    assert booking_details["departureDatetime"] == datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    assert booking_details["paymentStatus"] == False
    assert booking_details["companions"] == [
        (
            "George Arthur Collins Cooke",
            date(2009, 5, 7),
            "1A",
            1
        ),
        (
            "Jamie Allsop",
            date(2009, 5, 7),
            "1B",
            2
        ),
        (
            "Akil Rameez",
            date(2009, 5, 7),
            "1C",
            3
        )
    ]

def test_get_booking_Details_invalid_booking_does_not_exist(session: Session):
    LOGGER.error("Expecting error")

    with raises(ExistenceException):
        get_booking_details(session, 1)