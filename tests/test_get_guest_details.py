import pytest
from pytest import raises
from users import add_guest, add_airline_employee, get_guest_details
from sqlalchemy.orm import Session
import logging

from models import Guest

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_get_guest_details_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_guest_details(session, 1, "guest") == {
        "firstName": "George",
        "lastName": "Cooke",
        "email": "25cookeg899@collyers.ac.uk",
        "phone": "07802447086"
    }

def test_get_guest_details_all_valid_special(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_guest_details(session, 1, "admin") == {
        "firstName": "George",
        "lastName": "Cooke",
        "email": "25cookeg899@collyers.ac.uk",
        "phone": "07802447086",
        "password": "password123*"
    }

def test_get_guest_details_invalid_guest_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_guest_details(session, 1, "admin")

def test_get_guest_details_invalid_caller_type(session: Session):
    LOGGER.critical("Expecting error")

    with raises(Exception):
        get_guest_details(session, 1, "adminn")