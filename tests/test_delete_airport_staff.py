import pytest
from pytest import raises
from users import add_airport_staff, delete_airport_staff
from sqlalchemy.orm import Session
import logging

from models import AirportStaff

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_delete_airport_staff_all_valid(session: Session):
    add_airport_staff(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "password123*", "gate", "EGLL")
    
    delete_airport_staff(session, 1)

    assert session.query(AirportStaff).count() == 0

def test_delete_airport_staff_all_valid_multiple_in_table(session: Session):
    add_airport_staff(session, "Jamie", "Allsop", "25allsopj110@collyers.ac.uk", "password123*", "check-in", "EGLL")
    add_airport_staff(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "password123*", "gate", "EGLL")

    delete_airport_staff(session, 1)

    assert session.query(AirportStaff).count() == 1
    assert session.query(AirportStaff).filter(AirportStaff.airport_staff_id == 2) != None

def test_delete_airport_staff_staff_member_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        delete_airport_staff(session, 1)