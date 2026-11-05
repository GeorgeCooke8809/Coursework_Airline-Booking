import pytest
from pytest import raises
from users import add_guest, add_airline_employee, add_companion
from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta

from models import Guest

from utils.exceptions import ExistenceException, PassportException

LOGGER = logging.getLogger(__name__)

def test_add_companion_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_guest_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")

    with raises(ExistenceException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_name_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, True, date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_name_too_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cookfgekvekhvhekvbeluhbeuhbeubhleuhbefluubhleubuhelubhele", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_name_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_expiry_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", "05.11.2026", "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_expiry_past(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() - timedelta(days=1), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_number_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), 123456789, date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_number_long(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123uuftffyuyfiuf456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_passport_number_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "", date(2009, 5, 7), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_date_of_birth_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", "07.05.2009", "British Citizen", "M", "HMPO")

def test_add_companion_invalid_date_of_birth_future(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date.today() + timedelta(days=1), "British Citizen", "M", "HMPO")

def test_add_companion_invalid_nationality_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), True, "M", "HMPO")

def test_add_companion_invalid_nationality_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "", "M", "HMPO")

def test_add_companion_invalid_passport_sex_invalid(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "P", "HMPO")

def test_add_companion_invalid_passport_authority_type(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", True)

def test_add_companion_invalid_passport_authority_empty(session: Session):
    LOGGER.critical("Expecting error")

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    with raises(PassportException):
        add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "")