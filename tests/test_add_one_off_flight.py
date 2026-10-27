import pytest
from pytest import raises
from flights import create_route, add_one_off_flight
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_add_one_off_flight_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)

    add_one_off_flight(session, 1, datetime_occurs_on)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.route_id == 1
    assert service.start_date == service.end_date == datetime_occurs_on.date()
    assert service.repeat_type == "daily"
    assert service.repeat_time_utc == datetime_occurs_on.time()
    assert service.repeat_frequency == 1
    assert service.shown_in_list == False

    flight: Flight = (
        session.query(Flight)
        .filter(Flight.flight_id == 1)
    ).first()

    assert flight.service_id == 1
    assert flight.scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    assert flight.status == "scheduled"

def test_add_one_off_flight_invalid_route(session: Session):
    LOGGER.critical("Expecting error")

    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)


    with raises(ExistenceException):
        add_one_off_flight(session, 1, datetime_occurs_on)

def test_add_one_off_flight_invalid_date_type(session: Session):
    LOGGER.critical("Expecting error")

    create_route(session, "EGLL", "KJFK", 10_000)

    with raises(InvalidDateException):
        add_one_off_flight(session, 1, "11.12.2026 @ 11:30")

def test_add_one_off_flight_invalid_date_past(session: Session):
    LOGGER.critical("Expecting exception")

    create_route(session, "EGLL", "KJFK", 10_000)

    datetime_occurs_on = datetime.combine(date.today() - timedelta(days=1), time(11, 30), tzinfo=UTC)

    with raises(InvalidDateException):
        add_one_off_flight(session, 1, datetime_occurs_on)