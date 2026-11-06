import pytest
from pytest import raises

from users import add_airline_employee, add_guest
from bookings import batch_clear_unpaid_bookings, create_unpaid_booking
from flights import create_route, add_one_off_flight

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging

from models import Booking, Flight

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_batch_clear_uncleared_bookings_all_valid_one(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Guest
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    new_booking = Booking(flight_id=1, guest_id=1, datetime_booked = datetime.now() - timedelta(days = 8), payment_cleared=False)
    session.add(new_booking)

    session.commit()

    batch_clear_unpaid_bookings(session)

    assert session.query(Booking).count() == 0

def test_batch_clear_uncleared_bookings_all_valid_multiple(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Guest
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    create_unpaid_booking(session, 1, 1)

    new_booking = Booking(flight_id=1, guest_id=1, datetime_booked = datetime.now() - timedelta(days = 8), payment_cleared=False)
    session.add(new_booking)

    new_booking = Booking(flight_id=1, guest_id=1, datetime_booked = datetime.now() - timedelta(days = 10), payment_cleared=False)
    session.add(new_booking)

    new_booking = Booking(flight_id=1, guest_id=1, datetime_booked = datetime.now() - timedelta(days = 20), payment_cleared=True)
    session.add(new_booking)

    session.commit()

    batch_clear_unpaid_bookings(session)

    assert session.query(Booking).count() == 2