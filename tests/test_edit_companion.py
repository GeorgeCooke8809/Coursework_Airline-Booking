import pytest
from pytest import raises

from users import add_guest, add_airline_employee, add_companion, edit_companion
from bookings import create_unpaid_booking
from seats import add_booking_seat
from flights import create_route, add_one_off_flight

from sqlalchemy.orm import Session
import logging
from datetime import date, timedelta, time, UTC, datetime

from models import Companion

from utils.exceptions import ExistenceException, PassportException, CompanionException

LOGGER = logging.getLogger(__name__)

def test_add_companion_passport_name_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    edit_companion(session, 1, passport_name="Jamie Allsop")

    assert session.query(Companion).first().passport_name == "Jamie Allsop"

def test_add_companion_passport_name_invalid_type(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_name=True)

def test_add_companion_passport_name_invalid_long(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_name="Jamie Allsopjkhghjagvuheguhebuheubhelubheluhburhburbh Allsopjkhghjagvuheguhebuheubhelubheluhburhburbh Allsopjkhghjagvuheguhebuheubhelubheluhburhburbh")

def test_add_companion_passport_name_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_name="")



def test_add_companion_passport_expiry_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    edit_companion(session, 1, passport_expiry=date.today() + timedelta(days=15))

    assert session.query(Companion).first().passport_expiry == date.today() + timedelta(days=15)

def test_add_companion_passport_expiry_invalid_type(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_expiry=True)

def test_add_companion_passport_expiry_invalid_past(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_expiry=date.today() - timedelta(days=10))



def test_add_companion_passport_number_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    edit_companion(session, 1, passport_number="123456782")

    assert session.query(Companion).first().passport_number == "123456782"

def test_add_companion_passport_number_invalid_type(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_number=123456789)

def test_add_companion_passport_number_invalid_long(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_number="1234567890")

def test_add_companion_passport_number_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_number="")



def test_add_companion_date_of_birth_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    edit_companion(session, 1, date_of_birth=date.today() - timedelta(days=15))

    assert session.query(Companion).first().date_of_birth == date.today() - timedelta(days=15)

def test_add_companion_date_of_birth_invalid_type(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, date_of_birth=True)

def test_add_companion_date_of_birth_invalid_past(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, date_of_birth=date.today() + timedelta(days=10))



def test_add_companion_nationality_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    edit_companion(session, 1, nationality="United States")

    assert session.query(Companion).first().nationality == "United States"

def test_add_companion_nationality_invalid_type(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, nationality=True)

def test_add_companion_nationality_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, nationality="")



def test_add_companion_sex_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    edit_companion(session, 1, passport_sex="X")

    assert session.query(Companion).first().sex == "X"

def test_add_companion_sex_invalid(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_sex="P")



def test_add_companion_authority_all_valid(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    edit_companion(session, 1, passport_authority="USPO")

    assert session.query(Companion).first().passport_issue_authority == "USPO"

def test_add_companion_authority_invalid_type(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_authority=True)

def test_add_companion_authority_invalid_empty(session: Session):
    LOGGER.critical("Expecting error")
        
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    with raises(PassportException):
        edit_companion(session, 1, passport_authority="")


def test_add_companion_invalid_companion_does_not_exist(session: Session):
    LOGGER.critical("Expecting error")
        
    with raises(ExistenceException):
        edit_companion(session, 1, passport_authority="USPO")

def test_add_companion_invalid_empty_already_flown(session: Session):
    LOGGER.critical("Expecting error")
    create_route(session, "EGLL", "KJFK", 10_000)
    datetime_occurs_on = datetime.combine(date.today() + timedelta(days=1), time(11, 30), tzinfo=UTC)
    add_one_off_flight(session, 1, datetime_occurs_on)

    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    add_companion(session, 1, "George Arthur Collins Cooke", date.today() + timedelta(days=10), "123456789", date(2009, 5, 7), "British Citizen", "M", "HMPO")

    create_unpaid_booking(session, 1, 1)
    add_booking_seat(session, 1, 1, "1A")

    with raises(CompanionException):
        edit_companion(session, 1, passport_authority="USPO")