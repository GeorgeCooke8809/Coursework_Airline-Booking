import pytest
from pytest import raises, approx
from flights import create_route, add_one_off_flight, calculate_flight_duration
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_calculate_flight_duration_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    assert calculate_flight_duration(session, 1).total_seconds() == approx(6.919285563683485 * 3600)

def test_calculate_flight_duration_flight_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        calculate_flight_duration(session, 1)