import pytest
from pytest import raises

from users import add_airline_employee, add_guest
from bookings import create_unpaid_booking
from flights import create_route, add_one_off_flight, add_schedule

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight

from utils.exceptions import ExistenceException, InvalidDateException

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

    booking = (
        session.query(Booking)
    ).first()

    assert booking.guest_id == 1
    assert booking.flight_id == 1
    assert booking.payment_cleared == False

def test_create_unpaid_booking_invalid_guest_does_not_exit(session: Session):
    LOGGER.critical("Expecting error")

    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    with raises(ExistenceException):
        create_unpaid_booking(session, 1, 1)

def test_create_unpaid_booking_invalid_flight_does_not_exit(session: Session):
    LOGGER.critical("Expecting error")

    # Create Guest
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(ExistenceException):
        create_unpaid_booking(session, 1, 1)

def test_Create_unpaid_booking_invalid_flight_past(session: Session):
    LOGGER.critical("Expecting error")

    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "daily", 5, service_time) # ! I don't think the database will object if I add a flight that is before the start date of this if I do it bypassing the create one off flight that I used before

    datetime_occurs_on = datetime.combine(date.today() - timedelta(days=1), time(11, 30), tzinfo=UTC)
    new_flight = Flight(service_id=1, flight_number="262", scheduled_departure_datetime_utc=datetime_occurs_on, datetime_created_utc=datetime.now(tz=UTC), status="scheduled")
    session.add(new_flight)

    # Create Guest
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidDateException):
        create_unpaid_booking(session, 1, 1)