import pytest
from pytest import raises

from users import add_airline_employee, add_guest, add_companion
from bookings import create_unpaid_booking, get_all_guest_bookings
from flights import create_route, add_one_off_flight, change_flight_status
from seats import add_booking_seat

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, time, UTC
import logging
from pytz import timezone

from models import Booking, Flight, BookingSeat

from utils.exceptions import ExistenceException, SeatException

LOGGER = logging.getLogger(__name__)

def test_get_all_guest_bookings_all_valid(session: Session):
    # Create FLight
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=5), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    # Create Companion
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)
    add_booking_seat(session, 1, 1, "1A")

    create_unpaid_booking(session, 1, 2)
    add_booking_seat(session, 2, 1, "1A")

    change_flight_status(session, 2, "departed")

    all_guest_bookings = get_all_guest_bookings(session, 1)

    past_flight = all_guest_bookings["past"][0]
    future_flight = all_guest_bookings["future"][0]

    assert past_flight[0] == 2
    assert past_flight[1] == "London Heathrow Airport" # Departure Name
    assert past_flight[2] == "LHR" # Departure IATA
    assert past_flight[3] == datetime.combine(date.today() + timedelta(days=5), time(11, 30), tzinfo=UTC).astimezone(timezone("Europe/London")) # Departure local time
    assert past_flight[4] == "John F. Kennedy International Airport" # Destination name
    assert past_flight[5] == "JFK" # Destination IATA
    assert past_flight[8] == 1 # No COmpanions

    assert future_flight[0] == 1
    assert future_flight[1] == "London Heathrow Airport" # Departure Name
    assert future_flight[2] == "LHR" # Departure IATA
    assert future_flight[3] == datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC).astimezone(timezone("Europe/London")) # Departure local time
    assert future_flight[4] == "John F. Kennedy International Airport" # Destination name
    assert future_flight[5] == "JFK" # Destination IATA
    assert future_flight[8] == 1 # No COmpanions

def test_get_all_guest_bookings_invalid_guest_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_all_guest_bookings(session, 1)
