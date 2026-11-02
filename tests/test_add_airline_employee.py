import pytest
from pytest import raises
from users import add_guest, add_airline_employee
from sqlalchemy.orm import Session
import logging

from models import AirlineEmployee

from utils.exceptions import InvalidNameException, InvalidPhoneException, InvalidEmailException, InvalidPasswordException, EmployeeException

LOGGER = logging.getLogger(__name__)

def test_add_airline_employee_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    employee = (
        session.query(AirlineEmployee)
        .filter(AirlineEmployee.airline_employee_id == 1)
    ).first()

    assert employee.first_name == "Akil"
    assert employee.last_name == "Rameez"
    assert employee.email == "25arameez110@collyers.ac.uk"
    assert employee.phone == "07801447084"
    assert employee.password == "Password123*"
    assert employee.employee_type == "support"

def test_add_airline_employee_all_valid_no_surname(session: Session):
    add_airline_employee(session, "Akil", "", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    employee = (
        session.query(AirlineEmployee)
        .filter(AirlineEmployee.airline_employee_id == 1)
    ).first()

    assert employee.first_name == "Akil"
    assert employee.last_name == ""
    assert employee.email == "25arameez110@collyers.ac.uk"
    assert employee.phone == "07801447084"
    assert employee.password == "Password123*"
    assert employee.employee_type == "support"

def test_add_airline_employee_invalid_length_fname(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidNameException):
        add_airline_employee(session, "jkrhglkehrgljkjhergshlghslgbhlshuhiyg", "rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

def test_add_airline_employee_invalid_type_fname(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidNameException):
        add_airline_employee(session, True, "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

def test_add_airline_employee_invalid_length_lname(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidNameException):
        add_airline_employee(session, "Akil", "jkrhglkehrgljkjhergshlghslgbhlshuhiyg", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

def test_add_airline_employee_invalid_type_lname(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidNameException):
        add_airline_employee(session, "Akil", True, "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

def test_add_airline_employee_invalid_type_phone(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidPhoneException):
        add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", True, "Password123*", "support")

def test_add_airline_employee_invalid_length_phone(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidPhoneException):
        add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "123456789123456789", "Password123*", "support")

def test_add_airline_employee_invalid_content_phone(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidPhoneException):
        add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "hello", "Password123*", "support")

def test_add_airline_employee_invalid_email_format(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidEmailException):
        add_airline_employee(session, "Akil", "Rameez", "25arameez110collyers.ac.uk", "07802 4470896", "Password123*", "support")

def test_add_airline_employee_invalid_email_length(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidEmailException):
        add_airline_employee(session, "Akil", "Rameez", "jkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiyg@gmail.com", "07802 4470896", "Password123*", "support")

def test_add_airline_employee_invalid_password_type(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidPasswordException):
        add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", 1, "support")

def test_add_airline_employee_invalid_employee_type(session: Session):
    LOGGER.critical("Expecting error")
    with raises(EmployeeException):
        add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "supportt")