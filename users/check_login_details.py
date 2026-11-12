from models.base import with_session
from sqlalchemy.orm import Session
from sqlalchemy import literal

from models import Guest, AirlineEmployee, AirportStaff

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def check_login_details(Session: Session, email: str, password: str) -> dict | None:
    """Checks the login details provided. If details are correct, a dictionary with user ID and type is returned. If login details are incorrect, None is provided. Raises exception if email is used in multiple user databases.

    ## Return Format:
        {
            "id": <user_id>: int,
            "table": <user_table> str = "guest" | "airline" | "airport"
            "user_type": <user_type> str = "guest" | "support" | "operations" | "admin" | "gate" | "check-in"
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        email (str): The email of the user to check against
        password (str): The password to check against
    """
    # ? Switch to including admin, gate, check-in, ... ?

    LOGGER.info("Checking login details...")
    LOGGER.debug(f"{email = }")

    models = (
        (Guest, Guest.guest_id, literal("guest"), "guest"),
        (AirlineEmployee, AirlineEmployee.airline_employee_id, AirlineEmployee.employee_type,"airline"),
        (AirportStaff, AirportStaff.airport_staff_id, AirportStaff.staff_type, "airport")
    )

    for table, primary, secondary, table_name in models:
        user = (
            Session.query(primary, secondary)
            .filter(table.email == email)
            .filter(table.password == password)
        ).first()

        if user is not None:
            return {
                "id": user[0],
                "table": table_name,
                "user_type": user[1]
            }

    LOGGER.info("User does not exist.")