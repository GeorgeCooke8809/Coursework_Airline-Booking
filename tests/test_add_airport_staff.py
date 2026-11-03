import pytest
from pytest import raises
from users import add_airport_staff, add_airline_employee
from sqlalchemy.orm import Session
import logging

from models import AirportStaff

from utils.exceptions import InvalidNameException, InvalidEmailException, InvalidPasswordException, StaffException, InvalidAirportException

LOGGER = logging.getLogger(__name__)

def test_add_airport_staff_all_valid(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    staff_member = (
        session.query(AirportStaff)
        .filter(AirportStaff.airport_staff_id == 1)
    ).first()

    assert staff_member.first_name == "Jamie"
    assert staff_member.last_name == "Allsop"
    assert staff_member.email == "25jallsop110@collyers.ac.uk"
    assert staff_member.password == "password123*"
    assert staff_member.staff_type == "check-in"
    assert staff_member.assigned_airport_icao == "EGLL"

def test_add_airline_employee_all_valid_no_surname(session: Session):
    add_airport_staff(session, "Jamie", "", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    staff_member = (
        session.query(AirportStaff)
        .filter(AirportStaff.airport_staff_id == 1)
    ).first()

    assert staff_member.first_name == "Jamie"
    assert staff_member.last_name == ""
    assert staff_member.email == "25jallsop110@collyers.ac.uk"
    assert staff_member.password == "password123*"
    assert staff_member.staff_type == "check-in"
    assert staff_member.assigned_airport_icao == "EGLL"

def test_add_airline_employee_invalid_short_first_name(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidNameException):
        add_airport_staff(session, "", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airline_employee_invalid_long_first_name(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidNameException):
        add_airport_staff(session, "jkrhglkehrgljkjhergshlghslgbhlshuhiyg", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airport_staff_invalid_type_fname(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidNameException):
        add_airport_staff(session, 1, "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airport_staff_invalid_length_lname(session: Session):
    LOGGER.critical("Expecting error")
    with raises(InvalidNameException):
        add_airport_staff(session, "Jamie", "jkrhglkehrgljkjhergshlghslgbhlshuhiyg", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airport_staff_invalid_type_lname(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidNameException):
        add_airport_staff(session, "Jamie", 1, "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airport_staff_invalid_email_length(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidEmailException):
        add_airport_staff(session, "Jamie", "Allsop", "jkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiygjkrhglkehrgljkjhergshlghslgbhlshuhiyg@collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airport_staff_invalid_email_format(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidEmailException):
        add_airport_staff(session, "Jamie", "Allsop", "25jallsop110collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airport_staff_invalid_password_type(session: Session):
    LOGGER.critical("Expecting error")

    with raises(InvalidPasswordException):
        add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", True, "check-in", "EGLL")

def test_add_airport_staff_invalid_staff_type(session: Session):
    LOGGER.critical("Expecting error")

    with raises(StaffException):
        add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-inn", "EGLL")

def test_add_airport_staff_invalid_icao(session: Session):
    LOGGER.critical("Expecting error.")

    with raises(InvalidAirportException):
        add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLLL")

def test_add_airport_staff_invalid_email_already_in_use_same_table(session: Session):
    LOGGER.critical("Expecting error")
    add_airport_staff(session, "Jamie", "", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    with raises(InvalidEmailException):
        add_airport_staff(session, "Jamie", "", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

def test_add_airport_staff_invalid_email_already_in_use_different_table(session: Session):
    LOGGER.critical("Expecting error")
    add_airline_employee(session, "George", "Cooke", "25jallsop110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    with raises(InvalidEmailException):
            add_airport_staff(session, "Jamie", "", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")