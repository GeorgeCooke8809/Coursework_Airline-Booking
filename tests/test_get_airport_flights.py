import pytest
from pytest import raises
from flights import create_route, add_one_off_flight, get_airport_flights
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, InvalidDateException, InvalidAirportException

LOGGER = logging.getLogger(__name__)

def test_get_one_off_flight_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on_one = datetime.now() + timedelta(hours=1)
    add_one_off_flight(session, 1, datetime.combine(date=datetime_occurs_on_one.date(), time=datetime_occurs_on_one.time(), tzinfo=UTC))

    datetime_occurs_on_two = datetime.now() + timedelta(hours=2)
    add_one_off_flight(session, 1, datetime.combine(date=datetime_occurs_on_two.date(), time=datetime_occurs_on_two.time(), tzinfo=UTC))

    result = get_airport_flights(session, "EGLL")

    assert result[0][1:] == (
        "KJFK",
        "John F. Kennedy International Airport",
        datetime_occurs_on_one.time().strftime("%H:%M"),
        datetime_occurs_on_one - timedelta(minutes=30),
        datetime_occurs_on_one - timedelta(minutes=90)
    )

    assert result[1][1:] == (
        "KJFK",
        "John F. Kennedy International Airport",
        datetime_occurs_on_two.time().strftime("%H:%M"),
        datetime_occurs_on_two - timedelta(minutes=30),
        datetime_occurs_on_two - timedelta(minutes=90)
    )

def test_get_one_off_flight_no_results(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    assert get_airport_flights(session, "EGLL") == []

def test_get_one_off_flight_flights_are_at_other_airports(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
        
    datetime_occurs_on_one = datetime.now() + timedelta(hours=1)
    add_one_off_flight(session, 1, datetime.combine(date=datetime_occurs_on_one.date(), time=datetime_occurs_on_one.time(), tzinfo=UTC))

    datetime_occurs_on_two = datetime.now() + timedelta(hours=2)
    add_one_off_flight(session, 1, datetime.combine(date=datetime_occurs_on_two.date(), time=datetime_occurs_on_two.time(), tzinfo=UTC))

    assert get_airport_flights(session, "KJFK") == []

def test_get_one_off_flight_invalid_airport(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidAirportException):
        get_airport_flights(session, "Airport")