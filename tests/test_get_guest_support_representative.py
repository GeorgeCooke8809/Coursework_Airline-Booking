import pytest
from pytest import raises
from users import add_guest, add_airline_employee, get_guest_support_representative, delete_airline_employee
from sqlalchemy.orm import Session
import logging

from models import Guest

from utils.exceptions import InvalidNameException, InvalidPhoneException, InvalidEmailException, InvalidPasswordException, ExistenceException

LOGGER = logging.getLogger(__name__)

def test_get_guest_support_representative_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_guest_support_representative(session, 1) == {
        "id": 1,
        "firstName": "Akil",
        "lastName": "Rameez",
        "phoneNo": "07801447084"
    }

def test_get_guest_support_representative_no_guest_exists(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        get_guest_support_representative(session, 1)

def test_get_guest_support_representative_original_representative_deleted(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_airline_employee(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    delete_airline_employee(session, 1)

    assert get_guest_support_representative(session, 1) == {
        "id": 2,
        "firstName": "Jamie",
        "lastName": "Allsop",
        "phoneNo": "07801447084"
    }