import pytest
from pytest import raises
from users import add_airport_staff, edit_airport_staff_member
from sqlalchemy.orm import Session
import logging

from models import AirportStaff

from utils.exceptions import InvalidNameException, InvalidEmailException, InvalidPasswordException, StaffException, ExistenceException, InvalidAirportException

LOGGER = logging.getLogger(__name__)

def test_edit_airport_staff_all_valid_edit_first_name(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    edit_airport_staff_member(session, 1, first_name="Arthur")

    assert session.query(AirportStaff).first().first_name == "Arthur"

def test_edit_airport_staff_first_name_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidNameException):
        edit_airport_staff_member(session, 1, first_name=True)

def test_edit_airport_staff_first_name_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidNameException):
        edit_airport_staff_member(session, 1, first_name="rgherlughlergheruighergherghergheuhglerhgeghelghleghelghergh")

def test_edit_airport_staff_first_name_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidNameException):
        edit_airport_staff_member(session, 1, first_name="")



def test_edit_airport_staff_all_valid_edit_last_name(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    edit_airport_staff_member(session, 1, last_name="Collins")

    assert session.query(AirportStaff).first().last_name == "Collins"

def test_edit_airport_staff_last_name_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidNameException):
        edit_airport_staff_member(session, 1, last_name=True)

def test_edit_airport_staff_last_name_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidNameException):
        edit_airport_staff_member(session, 1, last_name="gjkherughergheroiugheriogherogheougheiougheirugheruighergheh")



def test_edit_airport_staff_email_all_valid(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    edit_airport_staff_member(session, 1, email="25allsopj110@collyers.ac.uk")

    assert session.query(AirportStaff).first().email == "25allsopj110@collyers.ac.uk"

def test_edit_airport_staff_email_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidEmailException):
        edit_airport_staff_member(session, 1, email=True)

def test_edit_airport_staff_email_invalid_format(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidEmailException):
        edit_airport_staff_member(session, 1, email="25cookeg899collyers.ac.uk")

def test_edit_airport_staff_email_invalid_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidEmailException):
        edit_airport_staff_member(session, 1, email="25cowigkehgkgkegegiegdgiuwhfwgfiuhwfgwfhwuifwuifhweuifhwgfwuigfwuigfiwgfuiwgfiuwgfeguigweuifghwuiergeiwgielghokeg899@collyers.ac.uk")

def test_edit_airport_staff_email_invalid_in_use(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")
    add_airport_staff(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidEmailException):
        edit_airport_staff_member(session, 1, email="25cookeg899@collyers.ac.uk")



def test_edit_airport_staff_password_all_valid(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    edit_airport_staff_member(session, 1, password="SuperPassword123*")

    assert session.query(AirportStaff).first().password == "SuperPassword123*"

def test_edit_airport_staff_password_invalid_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidPasswordException):
        edit_airport_staff_member(session, 1, password=True)

def test_edit_airport_staff_password_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidPasswordException):
        edit_airport_staff_member(session, 1, password="")



def test_edit_airport_staff_type_all_valid(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    edit_airport_staff_member(session, 1, staff_type="gate")

    assert session.query(AirportStaff).first().staff_type == "gate"

def test_edit_airport_staff_type_invalid_option(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(StaffException):
        edit_airport_staff_member(session, 1, staff_type="fired")



def test_edit_airport_staff_airport_all_valid(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    edit_airport_staff_member(session, 1, assigned_airport_icao="KJFK")

    assert session.query(AirportStaff).first().assigned_airport_icao == "KJFK"

def test_edit_airport_staff_airport_invalid_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidAirportException):
        edit_airport_staff_member(session, 1, assigned_airport_icao="KJFKK")