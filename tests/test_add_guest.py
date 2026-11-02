import pytest
from pytest import raises
from users import add_guest, add_airline_employee
from sqlalchemy.orm import Session
import logging

from models import Guest

from utils.exceptions import InvalidNameException, InvalidPhoneException, InvalidEmailException, InvalidPasswordException, ExistenceException

LOGGER = logging.getLogger(__name__)

def test_add_guest_all_valid(session: Session):
    add_airline_employee() # TODO: Implement

    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    guest = (
        session.query(Guest)
        .filter(Guest.guest_id == 1)
    ).first()

    assert guest.first_name == "George"