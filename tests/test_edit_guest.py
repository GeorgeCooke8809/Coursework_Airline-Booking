import pytest
from pytest import raises
from users import add_guest, add_airline_employee, edit_guest
from sqlalchemy.orm import Session
import logging

from models import Guest

from utils.exceptions import InvalidNameException, InvalidPhoneException, InvalidEmailException, InvalidPasswordException, ExistenceException

LOGGER = logging.getLogger(__name__)

def test_edit_guest_all_valid_edit_airline_employee(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_airline_employee(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    edit_guest(session, 1, airline_employee_id=2)

    assert session.query(Guest).first().customer_support_rep.first_name == "Jamie"

def test_edit_guest_invalid_edit_airline_employee_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(ExistenceException):
        edit_guest(session, 1, airline_employee_id=2)

def test_edit_guest_invalid_edit_airline_employee_of_wrong_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_airline_employee(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "07801 447084", "Password123*", "admin")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(ExistenceException):
        edit_guest(session, 1, airline_employee_id=2)



def test_edit_guest_all_valid_edit_first_name(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    edit_guest(session, 1, first_name="Arthur")

    assert session.query(Guest).first().first_name == "Arthur"

def test_edit_guest_first_name_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidNameException):
        edit_guest(session, 1, first_name=True)

def test_edit_guest_first_name_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidNameException):
        edit_guest(session, 1, first_name="rgherlughlergheruighergherghergheuhglerhgeghelghleghelghergh")

def test_edit_guest_first_name_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidNameException):
        edit_guest(session, 1, first_name="")



def test_edit_guest_all_valid_edit_last_name(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    edit_guest(session, 1, last_name="Collins")

    assert session.query(Guest).first().last_name == "Collins"

def test_edit_guest_last_name_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidNameException):
        edit_guest(session, 1, last_name=True)

def test_edit_guest_last_name_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidNameException):
        edit_guest(session, 1, last_name="gjkherughergheroiugheriogherogheougheiougheirugheruighergheh")



def test_edit_guest_email_all_valid(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    edit_guest(session, 1, email="25allsopj110@collyers.ac.uk")

    assert session.query(Guest).first().email == "25allsopj110@collyers.ac.uk"

def test_edit_guest_email_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidEmailException):
        edit_guest(session, 1, email=True)

def test_edit_guest_email_invalid_format(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidEmailException):
        edit_guest(session, 1, email="25cookeg899collyers.ac.uk")

def test_edit_guest_email_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidEmailException):
        edit_guest(session, 1, email="25cowigkehgkgkegegiegdgiuwhfwgfiuhwfgwfhwuifwuifhweuifhwgfwuigfwuigfiwgfuiwgfiuwgfeguigweuifghwuiergeiwgielghokeg899@collyers.ac.uk")

def test_edit_guest_email_invalid_in_use(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidEmailException):
        edit_guest(session, 1, email="25arameez110@collyers.ac.uk")



def test_edit_guest_phone_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    edit_guest(session, 1, phone="07802 447082")

    assert session.query(Guest).first().phone == "07802447082"

def test_edit_guest_phone_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidPhoneException):
        edit_guest(session, 1, phone=999)

def test_edit_guest_phone_invalid_numeric(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidPhoneException):
        edit_guest(session, 1, phone="Arthur")

def test_edit_guest_phone_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidPhoneException):
        edit_guest(session, 1, phone="1234567890123456789")

def test_edit_guest_phone_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidPhoneException):
        edit_guest(session, 1, phone="")



def test_edit_guest_password_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    edit_guest(session, 1, password="SuperPassword123*")

    assert session.query(Guest).first().password == "SuperPassword123*"

def test_edit_guest_password_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidPasswordException):
        edit_guest(session, 1, password=True)

def test_edit_guest_password_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(InvalidPasswordException):
        edit_guest(session, 1, password="")