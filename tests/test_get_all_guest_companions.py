import pytest
from pytest import raises
from users import add_guest, add_airline_employee, add_companion, get_all_guest_companions, disable_companion
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta

from models import Guest

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_get_all_guest_companions_valid_one(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    assert get_all_guest_companions(session, 1) == [(
        1,
        "George Arthur Collins Cooke",
        date(2009, 5, 7),
        date.today() + timedelta(days=10),
        "active",
        True
    )]

def test_get_all_guest_companions_valid_multiple(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")
    add_companion(session, 1, "Akil Rameez", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")
    add_companion(session, 1, "Jamie Allsop", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    disable_companion(session, 2)

    assert get_all_guest_companions(session, 1) == [
        (
            1,
            "George Arthur Collins Cooke",
            date(2009, 5, 7),
            date.today() + timedelta(days=10),
            "active",
            True
        ),
        (
            2,
            "Akil Rameez",
            date(2009, 5, 7),
            date.today() + timedelta(days=10),
            "inactive",
            False
        ),
        (
            3,
            "Jamie Allsop",
            date(2009, 5, 7),
            date.today() + timedelta(days=10),
            "active",
            False
        )
    ]

def test_get_all_guest_companions_valid_empty(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_all_guest_companions(session, 1) == []

def test_get_all_guest_companion_invalid_guest_does_not_exist(session: Session):
    LOGGER.critical("Expecting exception")

    with raises(ExistenceException):
        get_all_guest_companions(session, 1)