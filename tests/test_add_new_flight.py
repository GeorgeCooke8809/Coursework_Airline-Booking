import pytest
from pytest import raises
from flights import create_route, add_schedule, add_new_flight
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_add_new_flight_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

    add_new_flight(session, 1, datetime.combine(start_date, service_time, tzinfo=UTC))

    flight = (
        session.query(Flight)
        .filter(Flight.flight_id == 1)
    ).first()

    assert flight.service_id == 1
    assert flight.scheduled_departure_datetime_utc == datetime.combine(start_date, service_time)

def test_add_new_flight_invalid_service(session: Session):
    LOGGER.critical("Expecting exception...")

    start_date = date.today() + timedelta(days=1)
    service_time = time(11, 30, 0)

    with raises(ExistenceException):
        add_new_flight(session, 1, datetime.combine(start_date, service_time, tzinfo=UTC))

def test_add_new_flight_invalid_departure_datetime_type(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

    with raises(InvalidDateException):
        add_new_flight(session, 1, "11.12.2026 @ 11:30")

def test_add_new_flight_invalid_departure_datetime_past(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

    flight_datetime = datetime.combine(date.today() - timedelta(days=1), time(11,30), tzinfo=UTC)

    with raises(InvalidDateException):
        add_new_flight(session, 1, flight_datetime)