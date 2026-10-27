import pytest
from pytest import raises
from flights import create_route, add_schedule, edit_schedule
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time

from models import Service

from utils.exceptions import ExistenceException, RepeatException, InvalidDateException, InvalidTimeException
LOGGER = logging.getLogger(__name__)

def test_edit_schedule_all_fields_valid_daily(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)

    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "daily", 1, repeat_time)

    end_date = date.today() + timedelta(days = 8)
    repeat_time = time(12, 30, 0)

    edit_schedule(session, 1, end_date, "daily", 2, repeat_time)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.end_date == end_date
    assert service.repeat_type == "daily"
    assert service.repeat_frequency == 2
    assert service.repeat_time_utc == repeat_time

def test_edit_schedule_all_fields_valid_weekly(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "weekly", 1, repeat_time, 5)

    end_date = date.today() + timedelta(days = 8)
    repeat_time = time(12, 30, 0)

    edit_schedule(session, 1, end_date, "weekly", 2, repeat_time, 7)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.end_date == end_date
    assert service.repeat_type == "weekly"
    assert service.repeat_frequency == 2
    assert service.repeat_time_utc == repeat_time
    assert service.repeats_on == 7

def test_edit_schedule_all_fields_valid_monthly(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    end_date = date.today() + timedelta(days = 8)
    repeat_time = time(12, 30, 0)

    edit_schedule(session, 1, end_date, "monthly", 2, repeat_time, 15)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.end_date == end_date
    assert service.repeat_type == "monthly"
    assert service.repeat_frequency == 2
    assert service.repeat_time_utc == repeat_time
    assert service.repeats_on == 15

def test_edit_schedule_change_repeat_type_valid(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
        
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    end_date = date.today() + timedelta(days = 8)
    repeat_time = time(12, 30, 0)

    edit_schedule(session, 1, end_date, "weekly", 2, repeat_time, 5)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.end_date == end_date
    assert service.repeat_type == "weekly"
    assert service.repeat_frequency == 2
    assert service.repeat_time_utc == repeat_time
    assert service.repeats_on == 5

def test_edit_schedule_end_date_only(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
            
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    end_date = date.today() + timedelta(days = 8)

    edit_schedule(session, 1, end_date=end_date)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.end_date == end_date

def test_edit_schedule_repeat_type_only(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
            
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    edit_schedule(session, 1, repeat_type="weekly")

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.repeat_type == "weekly"

def test_edit_schedule_frequency_only(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
            
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    edit_schedule(session, 1, frequency=5)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.repeat_frequency == 5

def test_edit_schedule_time_only(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
            
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    edit_schedule(session, 1, scheduled_time=time(12, 30, 0))

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.repeat_time_utc == time(12, 30, 0)

def test_edit_schedule_repeats_on_only(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
            
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    edit_schedule(session, 1, repeats_on=2)

    service = (
        session.query(Service)
        .filter(Service.service_id == 1)
    ).first()

    assert service.repeats_on == 2

def test_edit_schedule_invalid_service(session: Session):
    LOGGER.critical("Expecting error...")

    with raises(ExistenceException):
        edit_schedule(session, 1, repeats_on=2)

def test_edit_schedule_invalid_end_date(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
                
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    with raises(InvalidDateException):
        edit_schedule(session, 1, end_date="11.12.2026")

def test_edit_schedule_invalid_repeat_type(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
                
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    with raises(RepeatException):
        edit_schedule(session, 1, repeat_type="dailyy")

def test_edit_schedule_invalid_frequency_type(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
                
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    with raises(RepeatException):
        edit_schedule(session, 1, frequency="1")

def test_edit_schedule_invalid_frequency_value(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
                
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    with raises(RepeatException):
        edit_schedule(session, 1, frequency=-2)

def test_edit_schedule_invalid_time(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
                
    start_date = date.today() + timedelta(days = 5)
    end_date = date.today() + timedelta(days = 7)
    repeat_time = time(11, 30, 0)

    add_schedule(session, 1, start_date, end_date, "monthly", 1, repeat_time, 5)

    with raises(InvalidTimeException):
        edit_schedule(session, 1, scheduled_time="12:30")