import pytest
from pytest import raises
from flights import create_route, add_one_off_flight, calculate_seat_price
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_calculate_seat_price_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    assert calculate_seat_price(session, 1) == 10000

def test_calculate_seat_price_all_valid_multiple_seats(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    assert calculate_seat_price(session, 1, 5) == 50000

def test_calculate_seat_price_flight_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        calculate_seat_price(session, 1, 1)

def test_calculate_seat_price_invalid_number_of_seats_type(session: Session):
    LOGGER.critical("Expecting error")

    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    with raises(Exception):
        calculate_seat_price(session, 1, "5")

def test_calculate_seat_price_invalid_number_of_seats_value(session: Session):
    LOGGER.critical("Expecting error")
    
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    with raises(Exception):
        calculate_seat_price(session, 1, -1)