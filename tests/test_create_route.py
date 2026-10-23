import pytest
from flights import create_route
from sqlalchemy.orm import Session

from models import Route, Airport

def test_add_valid_route_valid_price(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)