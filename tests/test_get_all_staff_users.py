import pytest
from pytest import raises
from users import add_airline_employee, add_airport_staff, get_all_staff_users
from sqlalchemy.orm import Session
import logging

LOGGER = logging.getLogger(__name__)

def test_get_all_staff_users_all_valid_single(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")

    assert get_all_staff_users(session) == [(
        "support",
        "employee",
        1,
        "Akil",
        "Rameez"
    )]

def test_get_all_staff_users_all_valid_one_from_each_table(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")
    
    assert get_all_staff_users(session) == [
        (
            "check-in",
            "staff",
            1,
            "Jamie",
            "Allsop"
        ),
        (
            "support",
            "employee",
            1,
            "Akil",
            "Rameez"
        )
    ]

def test_get_all_staff_users_all_valid_multiple_from_each_table(session: Session):
    add_airline_employee(session, "Akil", "Rameez", "25arameez110@collyers.ac.uk", "07801 447084", "Password123*", "support")
    add_airline_employee(session, "George", "Cooke", "25cookeg899@collyers.ac.uk", "07801 447084", "Password123*", "admin")

    add_airport_staff(session, "Jamie", "Allsop", "25jallsop110@collyers.ac.uk", "password123*", "check-in", "EGLL")
    add_airport_staff(session, "Samuel", "Wickens", "25wickenss125@collyers.ac.uk", "password123*", "gate", "EGKK")
    
    assert get_all_staff_users(session) == [
        (
            "check-in",
            "staff",
            1,
            "Jamie",
            "Allsop"
        ),
        (
            "admin",
            "employee",
            2,
            "George",
            "Cooke"
        ),
        (
            "support",
            "employee",
            1,
            "Akil",
            "Rameez"
        ),
        (
            "gate",
            "staff",
            2,
            "Samuel",
            "Wickens"
        )
    ]

def test_get_all_staff_users_all_valid_none_exist(session: Session):
    assert get_all_staff_users(session) == []