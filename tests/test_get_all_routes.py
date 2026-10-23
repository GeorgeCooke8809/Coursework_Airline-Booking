import pytest
from flights import create_route, get_all_routes
from sqlalchemy.orm import Session
import logging

from models import Route, Airport

LOGGER = logging.getLogger(__name__)

def test_get_only_one_added(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    all_routes = get_all_routes(session)

    assert all_routes == [
        (
            1,
            "London Heathrow Airport",
            "John F. Kennedy International Airport"
        )
    ]

def test_get_three_added(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    create_route(session, "KJFK", "EGLL", 9_000)
    create_route(session, "EGLL", "OMDB", 25_000)

    all_routes = get_all_routes(session)

    assert all_routes == [
        (
            1,
            "London Heathrow Airport",
            "John F. Kennedy International Airport"
        ),
        (
            2,
            "John F. Kennedy International Airport",
            "London Heathrow Airport"
        ),
        (
            3,
            "London Heathrow Airport",
            "Dubai International Airport"
        )
    ]