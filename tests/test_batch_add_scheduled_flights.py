import pytest
from flights import create_route, add_schedule, batch_generate_scheduled_flights
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, datetime, UTC
from dateutil.relativedelta import relativedelta

from models import Route, Service, Flight

LOGGER = logging.getLogger(__name__)

def test_batch_generate_scheduled_flights_in_middle_of_batch_lookahead_daily(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=15)
    service_time = time(23, 59, 0)
    add_schedule(session, 1, start_date, end_date, "daily", 5, service_time)

    batch_generate_scheduled_flights(session)
    
    flights = (
        session.query(Flight)
        .order_by(Flight.flight_id)
    ).all()

    assert len(flights) == 3 # ! Will fail if test is run between 23:59 and 00:00 - unlikely
    assert flights[0].scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=1), time(23,59))
    assert flights[-1].scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=11), time(23,59)) # FLights are on (days after current day): 1, 6, 11, 16, ... (16 and beyond falls outside of end date)

def test_batch_generate_scheduled_flights_in_middle_of_batch_lookahead_weekly(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=22)
    service_time = time(23, 59, 0)
    add_schedule(session, 1, start_date, end_date, "weekly", 1, service_time, repeats_on=start_date.weekday()) # Repeats on whatever the current day of the week is

    batch_generate_scheduled_flights(session)
    
    flights = (
        session.query(Flight)
        .order_by(Flight.flight_id)
    ).all()

    assert len(flights) == 4 # ! Will fail if test is run between 23:59 and 00:00 - unlikely
    assert flights[0].scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=1), time(23,59))
    assert flights[-1].scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=22), time(23,59)) # FLights are on (days after current day): 1, 8, 15, 22, 29, ... (29 and beyond falls outside of end date)

def test_batch_generate_scheduled_flights_in_middle_of_batch_lookahead_monthly(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    start_date = date.today() + relativedelta(months=1, day=5)
    end_date = date.today() + relativedelta(months=2, day=5)
    service_time = time(23, 59, 0)
    add_schedule(session, 1, start_date, end_date, "monthly", 1, service_time, repeats_on=start_date.day)

    batch_generate_scheduled_flights(session)

    flights = (
        session.query(Flight)
        .order_by(Flight.flight_id)
    ).all()

    assert len(flights) == 2 # ! Will fail if test is run between 23:59 and 00:00 - unlikely
    assert flights[0].scheduled_departure_datetime_utc == datetime.combine(date.today() + relativedelta(months=1, day=5), time(23,59))
    assert flights[-1].scheduled_departure_datetime_utc == datetime.combine(date.today() + relativedelta(months=2, day=5), time(23,59))

def test_batch_generate_scheduled_flights_over_batch_generate_period(session: Session):
    create_route(session, "EGLL", "KJFK", 10_000)
    
    start_date = date.today() + timedelta(days=89)
    end_date = date.today() + timedelta(days=91)
    service_time = time(23, 59, 0)
    add_schedule(session, 1, start_date, end_date, "daily", 1, service_time)

    batch_generate_scheduled_flights(session)

    flights = (
        session.query(Flight)
        .order_by(Flight.flight_id)
    ).all()

    assert len(flights) == 2 # ! Will fail if test is run between 23:59 and 00:00 - unlikely
    assert flights[0].scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=89), time(23,59))
    assert flights[-1].scheduled_departure_datetime_utc == datetime.combine(date.today() + timedelta(days=90), time(23,59))