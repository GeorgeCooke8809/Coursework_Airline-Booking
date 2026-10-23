import pytest
from pytest import raises
from flights import create_route
from sqlalchemy.orm import Session

from models import Route, Airport

from utils.exceptions import InvalidAirportException

def test_add_valid_route_valid_price(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    route: Route = (
        session.query(Route)
        .filter(Route.route_id == 1)
    ).first()

    assert route.origin_icao == "EGLL"
    assert route.origin == session.query(Airport).filter(Airport.icao == "EGLL").first()
    assert route.destination_icao == "KJFK"
    assert route.destination == session.query(Airport).filter(Airport.icao == "KJFK").first()
    assert route.price == 10_000
    assert route.services == []

def test_invalid_departure_airport_valid_arrival_airport_valid_price(session: Session):
    with raises(InvalidAirportException):
        create_route(session, "EGLLL", "KJFK", 10_000)

def test_valid_departure_airport_invalid_arrival_airport_valid_price(session: Session):
    with raises(InvalidAirportException):
        create_route(session, "EGLL", "KJFKK", 10_000)

def test_valid_departure_airport_valid_arrival_airport_invalid_price_type(session: Session):
    with raises(Exception):
        create_route(session, "EGLL", "KJFK", "£10,000")

def test_valid_departure_airport_valid_arrival_airport_invalid_price_magnitude(session: Session):
    with raises(Exception):
        create_route(session, "EGLL", "KJFK", -5)