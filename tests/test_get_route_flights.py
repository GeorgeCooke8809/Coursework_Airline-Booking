import pytest
from pytest import raises

from flights import create_route, add_schedule, add_new_flight, get_route_flights, add_one_off_flight
from users import add_airline_employee, add_guest, add_companion
from bookings import create_unpaid_booking
from seats import add_booking_seat

from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_get_route_flights_all_valid_one_in_each_no_bookings(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    add_schedule(session, 1, date.today(), date.today() + timedelta(days=10), "daily", 1, time(11, 30))

    # Past flight
    past_departure = datetime.now() - timedelta(days=3)
    new_flight = Flight(service_id=1, flight_number="262", scheduled_departure_datetime_utc=past_departure, datetime_created_utc=datetime.now(), status="departed")
    session.add(new_flight)
    session.commit()
    
    # Future flight
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    add_new_flight(session, 1, datetime_occurs_on.replace(tzinfo=UTC))

    assert get_route_flights(session, 1) == {
        "past": [(1, past_departure, 30, 0, "departed")],
        "future": [(2, datetime_occurs_on, 30, 0, "scheduled")]
    }

def test_get_route_flights_all_valid_multiple_in_each_no_bookings(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    add_schedule(session, 1, date.today(), date.today() + timedelta(days=10), "daily", 1, time(11, 30))

    # Past flight
    past_departure = datetime.now() - timedelta(days=3)
    new_flight = Flight(service_id=1, flight_number="262", scheduled_departure_datetime_utc=past_departure, datetime_created_utc=datetime.now(), status="departed")
    session.add(new_flight)

    new_flight = Flight(service_id=1, flight_number="263", scheduled_departure_datetime_utc=past_departure + timedelta(days=1), datetime_created_utc=datetime.now(), status="cancelled")
    session.add(new_flight)
    session.commit()
    
    # Future flight
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    add_new_flight(session, 1, datetime_occurs_on.replace(tzinfo=UTC))

    add_new_flight(session, 1, datetime_occurs_on.replace(tzinfo=UTC) + timedelta(days=3))

    assert get_route_flights(session, 1) == {
        "past": [(1, past_departure, 30, 0, "departed"), (2, past_departure + timedelta(days=1), 30, 0, "cancelled")],
        "future": [(3, datetime_occurs_on, 30, 0, "scheduled"), (4, datetime_occurs_on + timedelta(days=3), 30, 0, "scheduled")]
    }

def test_get_route_flights_all_valid_empty(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    assert get_route_flights(session, 1) == {
        "past": [],
        "future": []
    }

def test_get_route_flights_all_valid_passengers(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    add_one_off_flight(session, 1, datetime_occurs_on.replace(tzinfo=UTC))

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)

    # Actual test
    add_booking_seat(session, 1, 1, "1A")

    assert get_route_flights(session, 1) == {
        "past": [],
        "future": [(1, datetime_occurs_on, 30, 1, "scheduled")]
    }

def test_get_route_flights_invalid_route_does_not_exit(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_route_flights(session, 1)