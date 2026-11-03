import pytest
from pytest import raises
from users import add_airline_employee, delete_airline_employee
from sqlalchemy.orm import Session
import logging

from models import AirlineEmployee

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_delete_airline_employee_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    
    delete_airline_employee(session, 1)

    assert session.query(AirlineEmployee).count() == 0

def test_delete_airline_employee_all_valid_multiple_in_table(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "support")

    delete_airline_employee(session, 1)

    assert session.query(AirlineEmployee).count() == 1
    assert session.query(AirlineEmployee).filter(AirlineEmployee.airline_employee_id == 2) != None

def test_delete_airline_employee_employee_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        delete_airline_employee(session, 1)