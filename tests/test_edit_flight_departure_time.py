import pytest
from pytest import raises
from flights import create_route, add_one_off_flight, edit_flight_departure_time, change_flight_status
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, FlightStatusException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_edit_flight_departure_time_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    flight = (
        session.query(Flight)
        .filter(Flight.flight_id == 1)
    ).first()
    
    assert flight.scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=1), time(11, 30))

    new_time = datetime.now(tz=UTC) + timedelta(hours=5)

    edit_flight_departure_time(session, 1, new_time)

    flight = (
        session.query(Flight)
        .filter(Flight.flight_id == 1)
    ).first()
    
    assert flight.scheduled_departure_datetime_utc == new_time

def test_edit_flight_departure_time_flight_does_not_exit(session: Session):
    LOGGER.critical("Expecting error")

    new_time = datetime.now(tz=UTC) + timedelta(hours=5)

    with raises(ExistenceException):
        edit_flight_departure_time(session, 1, new_time)

def test_edit_flight_departure_time_invalid_flight_status(session: Session):
    LOGGER.critical("Expecting error")

    create_route(session, "EGLL", "KJFK", 10_000)
        
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    change_flight_status(session, 1, "departed")

    new_time = datetime.now(tz=UTC) + timedelta(hours=5)

    with raises(FlightStatusException):
        edit_flight_departure_time(session, 1, new_time)

def test_edit_flight_departure_time_invalid_time_format(session: Session):
    LOGGER.critical("Expecting error")
    
    create_route(session, "EGLL", "KJFK", 10_000)
        
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    with raises(InvalidDateException):
        edit_flight_departure_time(session, 1, "28.10.2026 @ 09:30")

def test_edit_flight_departure_time_invalid_time_past(session: Session):
    LOGGER.critical("Expecting error")
    
    create_route(session, "EGLL", "KJFK", 10_000)
        
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    new_time = datetime.now(tz=UTC) - timedelta(hours=5)

    with raises(InvalidDateException):
        edit_flight_departure_time(session, 1, new_time)