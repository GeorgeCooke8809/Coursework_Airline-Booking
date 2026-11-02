from models.base import with_session
from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Guest, AirlineEmployee, AirportStaff
from utils.exceptions import InvalidNameException, InvalidPhoneException, InvalidEmailException, InvalidPasswordException, ExistenceException

import logging
import re

LOGGER = logging.getLogger(__name__)

@with_session
def get_all_guest_users(Session: Session) -> list[tuple[int, str, str]]:
    """Gets and returns a list of all the guest users.

    ## Return:
        [
            (
                <guest_id>: int,
                <guest_first_name>: str,
                <guest_last_name>: str
            )
        ]
    
    ## Arguments:
        Session (Session): The database session automatically provided by @with_session
    """

@with_session
def get_guest_details(Session: Session, guest_id: int, caller_type: str) -> dict:
    """Gets and returns the details for the given guest. Used in the guest profile page and customer support rep portal. Raises an exception if guest does not exist or if aller type is not guest, admin, or customer support rep

    ## Return Format:
        {
            "firstName": <first_name>: str,
            "lastName": <last_name>: str,
            "email": <email>: str,
            "phone": <phone_number>: str,
            "password" <password>: str - only sent if user type is admin or customer support rep
        }

    ## Args:
        Session (Session): The database session automatically provided by @with_session
        guest_id (int): The ID of the guest tpo retrieve the details from
        caller_type (str): The user type requesting the details.
    """

@with_session
def get_guest_support_representative(Session: Session, guest_id: int) -> dict:
    """Gets the details of the customer support representative for the given guest

    ## Return Format:
        {
            "id": <airline_employee_id>: int,
            "firstName": <first_name>: str,
            "lastName": <last_name>: str,
            "phoneNo": <phone_number>: str
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        guest_id (int): The ID of the guest to get the customer support rep of
    """

@with_session
def add_guest(Session: Session, first_name: str, last_name: str, email: str, phone: str, password: str) -> None:
    """Adds a new guest record. Raises an exception if the email is already used in guest, airline employees, or airport staff tables. Also raises exception if email or password is invalid format. Airline employee is assigned based on which has the fewest guests assigned

    Args:
        Session (Session): The database session automatically provided by @with_session
        first_name (str): The first name of the new guest.
        last_name (str): The last name of the new guest.
        email (str): The email of the new guest.
        phone (str): The phone number of the new guest.
        password (str): The password of the new guest.
    """
    LOGGER.info("Adding new guest...")
    LOGGER.debug(f"{first_name = }, {last_name = }, {email = }, {phone = }")

    # * Validation

    phone = phone.replace(" ", "") # Remove any spaces added to phone number

    if (
        type(first_name) != str
        or (type(last_name) != str and last_name is not None)
        or len(first_name) > 34
        or len(last_name) > 34
    ):
        LOGGER.error(f"An invalid name has been inputted {first_name = }, {last_name = }")
        raise InvalidNameException

    if not phone.isnumeric():
        LOGGER.error("A non-numeric phone number was given")
        raise InvalidPhoneException

    if len(phone) > 14:
        LOGGER.error("The phone number given was too long")
        raise InvalidPhoneException

    pattern = re.compile("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")
    if pattern.match(email) == None:
        LOGGER.error("Email is invalid format")
        raise InvalidEmailException

    if (password == None or type(password) != str):
        LOGGER.error("Invalid password was given")
        raise InvalidPasswordException

    # * Processing

    airline_employee = (
        Session.query(AirlineEmployee)
        .filter(AirlineEmployee.employee_type == "support")
        .order_by(func.count(AirlineEmployee.guests), AirlineEmployee.airline_employee_id)
    ).first()

    if airline_employee is None:
        LOGGER.error("There are no active customer support representatives, cannot assign one to guest. Failing.")
        raise ExistenceException

    new_guest = Guest(customer_support_rep=airline_employee, first_name=first_name, last_name=last_name, email=email, phone=phone, password=password)

    Session.add(new_guest)

    LOGGER.info("Successfully added new guest")
    

@with_session
def edit_guest(Session: Session, guest_id: int, airline_employee_id: int = None, first_name: str = None, last_name: str = None, email: str = None, phone: str = None, password: str = None) -> None:
    """Edits the details of the given guest. Raises an exception if the email is already used in guest, airline employees, or airport staff tables. Also raises exception if email or password is invalid format or if airline employee does not exist.

    Args:
        Session (Session): The database session automatically provided by @with_session
        guest_id (int): The ID of the guest to be edited
        airline_employee_id (int, optional): The ID of the new airline employee assigned the guest. Defaults to None.
        first_name (str, optional): The new first name of the guest. Defaults to None.
        last_name (str, optional): The new last name of the guest. Defaults to None.
        email (str, optional): The new email of the guest. Defaults to None.
        phone (str, optional): The new phone number of the guest. Defaults to None.
        password (str, optional): The new password of the guest. Defaults to None.
    """

@with_session
def delete_guest(Session: Session, guest_id: int) -> None:
    """Deletes the given guest from the database

    Args:
        Session (Session): The database session automatically provided by @with_session
        guest_id (int): The ID of the guest to delete
    """
    # ? Nullify guest ID from companions