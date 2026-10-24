import pytest
from pytest import raises
from flights import create_route, add_schedule, delete_schedule
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time

from models import Service

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_delete_service_all_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    add_schedule(
        session,
        route_id=1,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=2),
        repeat_type = "daily",
        frequency=1,
        repeat_time=time(11, 30, 0)
    )

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.route_id == 1
    assert service.start_date == date.today() + timedelta(days=1)
    assert service.end_date == date.today() + timedelta(days=2)
    assert service.repeat_type == "daily"
    assert service.repeat_frequency == 1
    assert service.repeat_time_utc == time(11, 30, 0)

    delete_schedule(session, 1)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service == None

def test_delete_service_does_not_exist(session: Session):
    with raises(ExistenceException):
        delete_schedule(session, 1)