import pytest
from pytest import raises
from flights import create_route, add_one_off_flight, change_flight_status
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, FlightStatusException

LOGGER = logging.getLogger(__name__)

def test_change_flight_status_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    flight = (
        session.query(Flight)
        .filter(Flight.flight_id == 1)
    ).first()
    
    assert flight.status == "scheduled"

    change_flight_status(session, 1, "departed")

    flight = (
        session.query(Flight)
        .filter(Flight.flight_id == 1)
    ).first()
    
    assert flight.status == "departed"

def test_change_flight_status_flight_does_not_exist(session: Session):
    LOGGER.critical("Expecting exception")

    with raises(ExistenceException):
        change_flight_status(session, 1, "departed")

def test_change_flight_status_invalid_status_option(session: Session):
    LOGGER.critical("Expecting exception")

    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    with raises(FlightStatusException):
        change_flight_status(session, 1, "delayedd")