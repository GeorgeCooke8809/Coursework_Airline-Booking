import pytest
from pytest import raises
from flights import create_route, add_schedule
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time

from models import Route, Service

from utils.exceptions import InvalidDateException, RepeatException, InvalidTimeException, ExistenceException

LOGGER = logging.getLogger(__name__)

def test_add_service_all_valid_daily(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.route_id == 1
    assert service.start_date == start_date
    assert service.end_date == end_date
    assert service.repeat_type == "daily"
    assert service.repeat_frequency == 5
    assert service.repeat_time_utc == service_time

def test_add_service_all_valid_weekly(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "weekly", 5, service_time, 5)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.route_id == 1
    assert service.start_date == start_date
    assert service.end_date == end_date
    assert service.repeat_type == "weekly"
    assert service.repeat_frequency == 5
    assert service.repeat_time_utc == service_time
    assert service.repeats_on == 5

def test_add_service_all_valid_monthly(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 5, service_time, 20)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.route_id == 1
    assert service.start_date == start_date
    assert service.end_date == end_date
    assert service.repeat_type == "monthly"
    assert service.repeat_frequency == 5
    assert service.repeat_time_utc == service_time
    assert service.repeats_on == 20

def test_add_service_invalid_repeat_type(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    with raises(RepeatException):
        add_schedule(session, 1, start_date, end_date, "dailyy", 5, service_time)

def test_add_service_same_start_end_date(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    schedule_date = date.today() + timedelta(days=1)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, schedule_date, schedule_date, "daily", 1, service_time)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.route_id == 1
    assert service.start_date == schedule_date
    assert service.end_date == schedule_date
    assert service.repeat_type == "daily"
    assert service.repeat_frequency == 1
    assert service.repeat_time_utc == service_time
    assert service.repeats_on == None

def test_add_service_end_before_start_date(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=5)
    end_date = date.today() + timedelta(days=4)
    service_time = time(11, 30, 0)

    with raises(InvalidDateException):
        add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

def test_add_service_start_date_past(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() - timedelta(days=5)
    end_date = date.today() + timedelta(days=4)
    service_time = time(11, 30, 0)

    with raises(InvalidDateException):
        add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

def test_add_service_wrong_data_type_service_time(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=4)
    service_time = "11:30"

    with raises(InvalidTimeException):
        add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

def test_add_service_wrong_data_type_start_date(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = "24/10/2026"
    end_date = date.today() + timedelta(days=4)
    service_time = time(11, 30, 0)

    with raises(InvalidDateException):
        add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

def test_add_service_wrong_data_type_end_date(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=4)
    end_date = "24/10/2026"
    service_time = time(11, 30, 0)

    with raises(InvalidDateException):
        add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

def test_add_service_invalid_booking_id(session: Session):
    LOGGER.critical("Expecting exception.")

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    with raises(ExistenceException):
        add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

def test_add_service_invalid_occurs_on_for_weekly_eight(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    with raises(RepeatException):
        add_schedule(session, 1, start_date, end_date, "weekly", 5, service_time, 8)

def test_add_service_invalid_occurs_on_for_weekly_zero(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    with raises(RepeatException):
        add_schedule(session, 1, start_date, end_date, "weekly", 5, service_time, 0)

def test_add_service_invalid_occurs_on_for_monthly_thirty_two(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    with raises(RepeatException):
        add_schedule(session, 1, start_date, end_date, "monthly", 5, service_time, 32)

def test_add_service_invalid_occurs_on_for_monthly_zero(session: Session):
    LOGGER.critical("Expecting exception.")
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    with raises(RepeatException):
        add_schedule(session, 1, start_date, end_date, "monthly", 5, service_time, 0)

def test_add_service_invalid_occurs_on_for_daily(session: Session, caplog):
    LOGGER.critical("Expecting warning.")
    caplog.set_level(logging.WARNING)
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=5)
    service_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "daily", 5, service_time, 1)

    assert "Repeat type is daily but repeats_on was given as 1. Resetting to None."