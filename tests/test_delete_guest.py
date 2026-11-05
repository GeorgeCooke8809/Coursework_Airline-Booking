import pytest
from pytest import raises
from users import add_guest, add_airline_employee, delete_guest
from sqlalchemy.orm import Session
import logging

from models import Guest

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_delete_guest_valid_no_companions(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    delete_guest(session, 1)

    count = session.query(Guest).count()

    assert count == 0

def test_delete_guest_valid_with_companions(session: Session):
    LOGGER.critical("Return when companions are added") # TODO: Can't test delete user with companions until companions are added

    assert False

def test_delete_guest_invalid_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        delete_guest(session, 1)