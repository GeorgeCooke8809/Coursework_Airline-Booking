import pytest
from pytest import raises

from users import add_airline_employee, add_guest
from bookings import create_unpaid_booking, pay_booking
from flights import create_route, add_one_off_flight

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_create_unpaid_booking_all_valid(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Guest
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    create_unpaid_booking(session, 1, 1)

    pay_booking(session, 1)

    assert session.query(Booking).first().payment_cleared == True

def test_pay_booking_booking_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        pay_booking(session, 1)