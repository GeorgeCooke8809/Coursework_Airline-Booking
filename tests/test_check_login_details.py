import pytest
from pytest import raises
from users import add_guest, add_airline_employee, add_airport_staff, check_login_details
from sqlalchemy.orm import Session
import logging

LOGGER = logging.getLogger(__name__)

def test_check_login_details_correct_guest(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert check_login_details(session, "25cookeg899@collyers.ac.uk", "password123*") == {"id": 1, "type": "guest"}

def test_check_login_details_incorrect_guest(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert check_login_details(session, "25cookeg899@collyers.ac.uk", "NOT_password123*") == None

def test_check_login_details_correct_airline(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    assert check_login_details(session, "25arameez110@collyers.ac.uk", "Password123*") == {"id": 1, "type": "airline"}

def test_check_login_details_incorrect_airline(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    assert check_login_details(session, "25arameez110@collyers.ac.uk", "NOT_password123*") == None

def test_check_login_details_correct_airport(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    assert check_login_details(session, "25jallsop110@collyers.ac.uk", "password123*") == {"id": 1, "type": "airport"}

def test_check_login_details_incorrect_airport(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")

    assert check_login_details(session, "25jallsop110@collyers.ac.uk", "NOT_password123*") == None

def test_check_login_details_no_email_in_table(session: Session):
    assert check_login_details(session, "25cookeg899@collyerd.ac.uk", "Password123*") == None