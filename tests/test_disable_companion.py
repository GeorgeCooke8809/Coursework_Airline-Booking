import pytest
from pytest import raises
from users import add_guest, add_airline_employee, add_companion, disable_companion
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta

from models import Companion

from utils.exceptions import ExistenceException

LOGGER = logging.getLogger(__name__)

def test_disable_companion_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    disable_companion(session, 1)

    companion = (
        session.query(Companion)
        .filter(Companion.companion_id == 1)
    ).first()

    assert companion.status == "inactive"

def test_disable_companion_companion_does_not_exits(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        disable_companion(session, 1)