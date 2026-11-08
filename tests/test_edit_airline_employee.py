import pytest
from pytest import raises
from users import add_airline_employee, edit_airline_employee, add_guest
from sqlalchemy.orm import Session
import logging

from models import AirlineEmployee, Guest

from utils.exceptions import InvalidNameException, InvalidPhoneException, InvalidEmailException, InvalidPasswordException, EmployeeException, ExistenceException

LOGGER = logging.getLogger(__name__)

def test_edit_airline_employee_all_valid_edit_first_name(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    edit_airline_employee(session, 1, first_name="Arthur")

    assert session.query(AirlineEmployee).first().first_name == "Arthur"

def test_edit_airline_employee_first_name_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        edit_airline_employee(session, 1, first_name=True)

def test_edit_airline_employee_first_name_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        edit_airline_employee(session, 1, first_name="rgherlughlergheruighergherghergheuhglerhgeghelghleghelghergh")

def test_edit_airline_employee_first_name_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        edit_airline_employee(session, 1, first_name="")



def test_edit_airline_employee_all_valid_edit_last_name(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    edit_airline_employee(session, 1, last_name="Collins")

    assert session.query(AirlineEmployee).first().last_name == "Collins"

def test_edit_airline_employee_last_name_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        edit_airline_employee(session, 1, last_name=True)

def test_edit_airline_employee_last_name_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidNameException):
        edit_airline_employee(session, 1, last_name="gjkherughergheroiugheriogherogheougheiougheirugheruighergheh")



def test_edit_airline_employee_email_all_valid(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    edit_airline_employee(session, 1, email="25allsopj110@collyers.ac.uk")

    assert session.query(AirlineEmployee).first().email == "25allsopj110@collyers.ac.uk"

def test_edit_airline_employee_email_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidEmailException):
        edit_airline_employee(session, 1, email=True)

def test_edit_airline_employee_email_invalid_format(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidEmailException):
        edit_airline_employee(session, 1, email="25cookeg899collyers.ac.uk")

def test_edit_airline_employee_email_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidEmailException):
        edit_airline_employee(session, 1, email="25cowigkehgkgkegegiegdgiuwhfwgfiuhwfgwfhwuifwuifhweuifhwgfwuigfwuigfiwgfuiwgfiuwgfeguigweuifghwuiergeiwgielghokeg899@collyers.ac.uk")

def test_edit_airline_employee_email_invalid_in_use(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_airline_employee(session, "Jamie", "Allsop", "25allsopj899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidEmailException):
        edit_airline_employee(session, 1, email="25allsopj899@collyers.ac.uk")



def test_edit_airline_employee_phone_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    edit_airline_employee(session, 1, phone="07802 447082")

    assert session.query(AirlineEmployee).first().phone == "07802447082"

def test_edit_airline_employee_phone_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPhoneException):
        edit_airline_employee(session, 1, phone=999)

def test_edit_airline_employee_phone_invalid_numeric(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPhoneException):
        edit_airline_employee(session, 1, phone="Arthur")

def test_edit_airline_employee_phone_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPhoneException):
        edit_airline_employee(session, 1, phone="1234567890123456789")

def test_edit_airline_employee_phone_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPhoneException):
        edit_airline_employee(session, 1, phone="")



def test_edit_airline_employee_password_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    edit_airline_employee(session, 1, password="SuperPassword123*")

    assert session.query(AirlineEmployee).first().password == "SuperPassword123*"

def test_edit_airline_employee_password_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPasswordException):
        edit_airline_employee(session, 1, password=True)

def test_edit_airline_employee_password_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidPasswordException):
        edit_airline_employee(session, 1, password="")



def test_edit_airline_employee_type_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "admin")

    edit_airline_employee(session, 1, employee_type="support")

    assert session.query(AirlineEmployee).first().employee_type == "support"

def test_edit_airline_employee_type_invalid_type(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "admin")

    with raises(EmployeeException):
        edit_airline_employee(session, 1, employee_type="supporttttt")

def test_edit_airline_employee_type_all_valid_from_support(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_airline_employee(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    edit_airline_employee(session, 1, employee_type="admin")

    assert session.query(Guest).first().airline_employee_id == 2