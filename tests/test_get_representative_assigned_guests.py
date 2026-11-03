import pytest
from pytest import raises
from users import add_guest, add_airline_employee, get_representative_assigned_guests
from sqlalchemy.orm import Session
import logging

from utils import ExistenceException

from models import Guest, AirlineEmployee

LOGGER = logging.getLogger(__name__)

def test_get_representative_assigned_guests_all_valid_one_no_flights(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_representative_assigned_guests(session, 1) == [(
        1,
        "George",
        "Cooke",
        None
    )]

def test_get_representative_assigned_guests_all_valid_multiple_no_flights(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")
    add_guest(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "07802 447086", "password123*")

    guests = get_representative_assigned_guests(session, 1)

    assert guests == [
        (
            2,
            "Jamie",
            "Allsop",
            None
        ),
        (
            1,
            "George",
            "Cooke",
            None
        )
    ]

def test_get_representative_assigned_guests_all_valid_one_with_flight(session: Session):
    # TODO: Come back to testing getting guest next flight in get_representative_assigned_guests - Waiting on users being able to book flights
    assert False

def test_get_representative_assigned_guests_no_guests(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    assert get_representative_assigned_guests(session, 1) == []

def test_get_representative_assigned_guests_no_employees(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_representative_assigned_guests(session, 1)

def test_get_representative_assigned_guests_no_representative(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "admin")

    with raises(ExistenceException):
        get_representative_assigned_guests(session, 1)