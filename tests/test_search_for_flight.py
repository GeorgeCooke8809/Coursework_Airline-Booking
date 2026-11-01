import pytest
from pytest import raises, approx
from flights import create_route, add_one_off_flight, search_for_flight
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC

from models import Route, Service, Flight

from utils.exceptions import ExistenceException, InvalidDateException

LOGGER = logging.getLogger(__name__)

def test_search_for_flight_all_valid_single_flight_full_airport_names(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    search_result = search_for_flight(session, "London Heathrow Airport", "John F. Kennedy International Airport", date.today() + timedelta(days=1))

    assert search_result[0][0] == 1
    assert search_result[0][1] == "London Heathrow Airport"
    assert search_result[0][2] == "LHR"
    assert search_result[0][3] == datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    assert search_result[0][4].total_seconds() == approx(6.919285563683485 * 3600)
    assert search_result[0][5] == "John F. Kennedy International Airport"
    assert search_result[0][6] == "JFK"
    assert search_result[0][7] == datetime.combine(date.today() + timedelta(days=1), time(11, 30)) + search_result[0][4]
    assert search_result[0][8] == 10_000

def test_search_for_flight_all_valid_single_flight_part_airport_names(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
        
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    search_result = search_for_flight(session, "Heathrow", "John F. Kennedy", date.today() + timedelta(days=1))

    assert search_result[0][0] == 1
    assert search_result[0][1] == "London Heathrow Airport"
    assert search_result[0][2] == "LHR"
    assert search_result[0][3] == datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    assert search_result[0][4].total_seconds() == approx(6.919285563683485 * 3600)
    assert search_result[0][5] == "John F. Kennedy International Airport"
    assert search_result[0][6] == "JFK"
    assert search_result[0][7] == datetime.combine(date.today() + timedelta(days=1), time(11, 30)) + search_result[0][4]
    assert search_result[0][8] == 10_000

def test_search_for_flight_all_valid_single_flight_full_iata_codes(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
        
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    search_result = search_for_flight(session, "LHR", "JFK", date.today() + timedelta(days=1))

    assert search_result[0][0] == 1
    assert search_result[0][1] == "London Heathrow Airport"
    assert search_result[0][2] == "LHR"
    assert search_result[0][3] == datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    assert search_result[0][4].total_seconds() == approx(6.919285563683485 * 3600)
    assert search_result[0][5] == "John F. Kennedy International Airport"
    assert search_result[0][6] == "JFK"
    assert search_result[0][7] == datetime.combine(date.today() + timedelta(days=1), time(11, 30)) + search_result[0][4]
    assert search_result[0][8] == 10_000

def test_search_for_flight_full_airport_names_multiple_flights(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(10, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    search_result = search_for_flight(session, "LHR", "JFK", date.today() + timedelta(days=1))
    
    assert search_result[0][0] == 2
    assert search_result[0][1] == "London Heathrow Airport"
    assert search_result[0][2] == "LHR"
    assert search_result[0][3] == datetime.combine(date.today() + timedelta(days=1), time(10, 30))
    assert search_result[0][4].total_seconds() == approx(6.919285563683485 * 3600)
    assert search_result[0][5] == "John F. Kennedy International Airport"
    assert search_result[0][6] == "JFK"
    assert search_result[0][7] == datetime.combine(date.today() + timedelta(days=1), time(10, 30)) + search_result[0][4]
    assert search_result[0][8] == 10_000

    assert search_result[1][0] == 1
    assert search_result[1][1] == "London Heathrow Airport"
    assert search_result[1][2] == "LHR"
    assert search_result[1][3] == datetime.combine(date.today() + timedelta(days=1), time(11, 30))
    assert search_result[1][4].total_seconds() == approx(6.919285563683485 * 3600)
    assert search_result[1][5] == "John F. Kennedy International Airport"
    assert search_result[1][6] == "JFK"
    assert search_result[1][7] == datetime.combine(date.today() + timedelta(days=1), time(11, 30)) + search_result[0][4]
    assert search_result[1][8] == 10_000

def test_search_for_flight_all_valid_no_flights_on_date(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    search_result = search_for_flight(session, "LHR", "JFK", date.today() + timedelta(days=2))

    assert search_result == []

def test_search_for_flight_all_valid_no_route(session: Session):
    search_result = search_for_flight(session, "LHR", "JFK", date.today() + timedelta(days=2))

    assert search_result == []

def test_search_for_flight_invalid_departure_date_type(session: Session):
    LOGGER.critical("Expecting error...")

    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    with raises(InvalidDateException):
        search_for_flight(session, "LHR", "JFK", "01.11.2026")

def test_search_for_flight_invalid_date_type_past(session: Session):
    LOGGER.critical("Expecting error...")
    
    create_route(session, "EGLL", "KJFK", 10_000)
    
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    with raises(InvalidDateException):
            search_for_flight(session, "LHR", "JFK", date.today() - timedelta(days=1))