import pytest
from pytest import raises
from users import add_guest, add_airline_employee, get_all_guest_users
from sqlalchemy.orm import Session
import logging

LOGGER = logging.getLogger(__name__)

def test_get_all_guest_users_none(session: Session):
    assert get_all_guest_users(session) == []

def test_get_all_guest_users_one(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_all_guest_users(session) == [(1, "George", "Cooke")]

def test_get_all_guest_users_two(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_guest(session, "Akil", "Rameez", "25rameeza154@collyers.ac.uk", "07802 447086", "password123*")
    add_guest(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07802 447086", "password123*")

    assert get_all_guest_users(session) == [(2, "George", "Cooke"), (1, "Akil", "Rameez")]