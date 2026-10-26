import pytest
from pytest import raises
from flights import create_route, add_schedule, get_route_schedules
from sqlalchemy.orm import Session
import logging
from datetime import date, time, timedelta

from models import Route, Airport, Service

from utils.exceptions import InvalidAirportException, ExistenceException

LOGGER = logging.getLogger(__name__)

def test_get_route_schedules_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    service = Service(
        route_id = 1,
        start_date = date.today() - timedelta(days=5),
        end_date = date.today() - timedelta(days=3),
        repeat_type = "daily",
        repeat_time_utc = time(11, 30, 0),
        repeat_frequency = 1,
        shown_in_list = True
    )
    session.add(service) # ID = 1

    service = Service(
        route_id = 1,
        start_date = date.today() - timedelta(days=5),
        end_date = date.today() - timedelta(days=2),
        repeat_type = "daily",
        repeat_time_utc = time(11, 30, 0),
        repeat_frequency = 1,
        shown_in_list = True
    )
    session.add(service) # ID = 2

    service = Service(
        route_id = 1,
        start_date = date.today() + timedelta(days=5),
        end_date = date.today() + timedelta(days=7),
        repeat_type = "daily",
        repeat_time_utc = time(11, 30, 0),
        repeat_frequency = 1,
        shown_in_list = True
    )
    session.add(service) # ID = 3

    service = Service(
        route_id = 1,
        start_date = date.today() + timedelta(days=2),
        end_date = date.today() + timedelta(days=7),
        repeat_type = "daily",
        repeat_time_utc = time(11, 30, 0),
        repeat_frequency = 1,
        shown_in_list = True
    )
    session.add(service) # ID = 4

    schedules = get_route_schedules(session, 1)

    assert schedules == {
        "past": [
            (
                1,
                "daily",
                1,
                None,
                time(11, 30, 0)
            ),
            (
                2,
                "daily",
                1,
                None,
                time(11, 30, 0)
            )
        ],
        "present": [
            (
                4,
                "daily",
                1,
                None,
                time(11, 30, 0)
            ),
            (
                3,
                "daily",
                1,
                None,
                time(11, 30, 0)
            )
        ],
    }

def test_get_route_schedules_empty(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    assert get_route_schedules(session, 1) == {
        "past": [],
        "present": []
    }

def test_get_route_schedules_no_route_exists(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_route_schedules(session, 1)