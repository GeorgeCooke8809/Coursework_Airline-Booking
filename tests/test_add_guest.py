import pytest
from pytest import raises
from users import add_guest, add_airline_employee
from sqlalchemy.orm import Session
import logging

from models import Guest

from utils.exceptions import InvalidNameException, InvalidPhoneException, InvalidEmailException, InvalidPasswordException, ExistenceException

LOGGER = logging.getLogger(__name__)

def test_add_guest_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    guest = (
        session.query(Guest)
        .filter(Guest.guest_id == 1)
    ).first()

    assert guest.first_name == "George"
    assert guest.last_name == "Cooke"
    assert guest.airline_employee_id == 1
    assert guest.email == "25cookeg899@collyers.ac.uk"
    assert guest.phone == "07802447086"
    assert guest.password == "password123*"

def test_add_guest_all_valid_no_surname(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    add_guest(session, "George", "", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    guest = (
        session.query(Guest)
        .filter(Guest.guest_id == 1)
    ).first()

    assert guest.first_name == "George"
    assert guest.last_name == ""
    assert guest.airline_employee_id == 1
    assert guest.email == "25cookeg899@collyers.ac.uk"
    assert guest.phone == "07802447086"
    assert guest.password == "password123*"

def test_add_guest_no_support_rep(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "admin")

    with raises(ExistenceException):
        add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

def test_add_guest_invalid_length_fname(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        add_guest(session, "jkrhglkehrgljkjhergshlghslgbhlshuhiyg", "rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*")

def test_add_guest_invalid_type_fname(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        add_guest(session, True, "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*")

def test_add_guest_invalid_length_lname(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        add_guest(session, "Akil", "jkrhglkehrgljkjhergshlghslgbhlshuhiyg", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*")

def test_add_guest_invalid_type_lname(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        add_guest(session, "Akil", True, "25arameez110@collyers.ac.uk", "07801 447084", "Password123*")

def test_add_guest_invalid_type_phone(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPhoneException):
        add_guest(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", True, "Password123*")

def test_add_guest_invalid_length_phone(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPhoneException):
        add_guest(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "123456789123456789", "Password123*")

def test_add_guest_invalid_content_phone(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPhoneException):
        add_guest(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "hello", "Password123*")

def test_add_guest_invalid_email_format(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidEmailException):
        add_guest(session, "Akil", "Rameez", "25arameez110collyers.ac.uk", "07802 4470896", "Password123*")

def test_add_guest_invalid_email_length(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidEmailException):
        add_guest(session, "Akil", "Rameez", "jkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiyg@gmail.com", "07802 4470896", "Password123*")

def test_add_guest_invalid_password_type(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")
    
    with raises(InvalidPasswordException):
        add_guest(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", 1)

def test_add_guest_email_already_in_use_same_table(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    add_guest(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*")
    
    with raises(InvalidEmailException):
        add_guest(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*")

def test_add_guest_email_already_in_use_different_table(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")
    
    with raises(InvalidEmailException):
        add_guest(session, "Akil", "Rameez", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*")