import pytest
from pytest import raises
from users import add_guest, add_airline_employee, add_companion, favourite_companion, disable_companion
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta

from models import Companion

from utils.exceptions import ExistenceException, CompanionException

LOGGER = logging.getLogger(__name__)

def test_favourite_companion_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO") # Automatically marked as favourite
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123406789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    favourite_companion(session, 2)

    assert session.query(Companion).filter(Companion.companion_id == 1).first().favorite == False
    assert session.query(Companion).filter(Companion.companion_id == 2).first().favorite == True

def test_favourite_companion_invalid_companion_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        favourite_companion(session, 1)

def test_favourite_companion_invalid_inactive(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO") # Automatically marked as favourite
    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123406789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    disable_companion(session, 2)

    with raises(CompanionException):
        favourite_companion(session, 2)

def test_favourite_companion_invalid_expired(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO") # Automatically marked as favourite

    new_companion = Companion(guest_id=1, passport_name="George Arthur Collins Cooke", passport_number="123406789", passport_expiry=date.today() - timedelta(days=10), nationality="British Citizen", passport_issue_authority="HMPO", date_of_birth=date(2009, 5, 7), sex="M", status="active", favorite=False)
    session.add(new_companion)

    session.commit()

    with raises(CompanionException):
        favourite_companion(session, 2)