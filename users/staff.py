from models.base import with_session
from sqlalchemy.orm import Session

from models import AirportStaff, AirlineEmployee, Guest, Booking, Flight, Airport
from models import AIRLINE_EMPLOYEE_TYPES, AIRPORT_STAFF_TYPES

from utils import (
    check_email_already_in_use,
    InvalidNameException,
    InvalidPhoneException,
    InvalidEmailException,
    InvalidPasswordException,
    EmployeeException,
    InvalidAirportException,
    StaffException,
    ExistenceException
)

from datetime import datetime
import logging
import re

LOGGER = logging.getLogger(__name__)

@with_session
def get_all_staff_users(Session: Session) -> list[tuple[str, str, int, str, str]]:
    """Gets and returns a list of all the staff users.
    
    ## Return:
        [
            (
                <staff_type>: str,
                <staff_table>: str,
                <staff_id>: int,
                <staff_first_name>: str,
                <staff_last_name>: str
            )
        ]

    ## Arguments:
        Session (Session): The database session automatically provided by @with_session
    """

@with_session
def add_airline_employee(Session: Session, first_name: str, last_name: str, email: str, phone: str, password: str, employee_type: str) -> None:
    """Adds a new airline employee with the given details. Raises exception if email, phone, or password are invalid format. Also raises exception if type is not in allowed airline employee types list. Also raises exception if email is in use in any other user table.

    Args:
        Session (Session): The database session automatically provided by @with_session
        first_name (str): The first name of the new airline employee
        last_name (str): The last name of the new airline employee
        email (str): The email of the new airline employee
        phone (str): The phone number of the new airline employee
        password (str): The password of the new airline employee
        type (str): The employee type of the new airline employee
    """
    LOGGER.info("Adding new airline employee...")
    LOGGER.debug(f"{first_name = }, {last_name = }, {email = }, {phone = }, {employee_type = }")

    # * Validation

    if (
        type(first_name) != str
        or (type(last_name) != str and last_name is not None)
        or len(first_name) > 34
        or len(first_name) < 1
        or len(last_name) > 34
    ):
        LOGGER.error(f"An invalid name has been inputted {first_name = }, {last_name = }")
        raise InvalidNameException

    if type(phone) != str:
        LOGGER.error("Phone number is of the wrong data type")
        raise InvalidPhoneException

    phone = phone.replace(" ", "") # Remove any spaces added to phone number

    if not phone.isnumeric():
        LOGGER.error("A non-numeric phone number was given")
        raise InvalidPhoneException

    if len(phone) > 14:
        LOGGER.error("The phone number given was too long")
        raise InvalidPhoneException

    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)") # Only checks correct format, does not confirm has not been misstyped of lied about
    if pattern.match(email) == None or len(email) > 124:
        LOGGER.error("Email is invalid format")
        raise InvalidEmailException

    if check_email_already_in_use(Session, email):
        LOGGER.error("The email is already in use")
        raise InvalidEmailException

    if type(password) != str:
        LOGGER.error("Invalid password was given")
        raise InvalidPasswordException

    if employee_type not in AIRLINE_EMPLOYEE_TYPES:
        LOGGER.error("Invalid employee_type given.")
        raise EmployeeException(f"The given employee type is invalid.\n{employee_type = } is not in {AIRLINE_EMPLOYEE_TYPES = }")

    # * Processing

    new_employee = AirlineEmployee(first_name=first_name, last_name=last_name, email=email, phone=phone, employee_type=employee_type, password=password)
    Session.add(new_employee)


@with_session
def edit_airline_employee(Session: Session, airline_employee_id: int, first_name: str = None, last_name: str = None, email: str = None, phone: str = None, password: str = None, type: str = None) -> None:
    """Edits the given airline employee. If current type is representative and moving away, reassigns guests to other representatives. Raises exception if email, phone, or password are invalid format. Also raises exception if type is not in allowed airline employee types list. Also raises exception if email is in use in any other user table.

    Args:
        Session (Session): The database session automatically provided by @with_session
        airline_employee_id (int): The ID of the airline employee to be edited
        first_name (str): The new first name of airline employee
        last_name (str): The new last name of the airline employee
        email (str): The new email of the airline employee
        phone (str): The new phone number of the airline employee
        password (str): The new password of the airline employee
        type (str): The new employee type of the airline employee
    """

@with_session
def delete_airline_employee(Session: Session, airline_employee_id: int) -> None:
    """Deletes the given airline employee. If they are a customer support rep, reassigns their guests by iteratively going through them and assigning them to the rep with the fewest assigned guests.

    Args:
        Session (Session): The database session automatically provided by @with_session
        airline_employee_id (int): The ID of the airline employee to be deleted.
    """
    LOGGER.info("Deleting airline employee member")
    LOGGER.debug(f"{airline_employee_id = }")

    employee = (
        Session.query(AirlineEmployee)
        .filter(AirlineEmployee.airline_employee_id == airline_employee_id)
    ).first()

    if employee == None:
        LOGGER.error("Airline employee does not exist")
        raise ExistenceException

    Session.delete(employee)


@with_session
def add_airport_staff(Session: Session, first_name: str, last_name: str, email: str, password: str, staff_type: str, assigned_airport_icao: str) -> None:
    """Adds a new airport staff record. Raises exception if email, or password are invalid format. Also raises exception if type is not in allowed airport staff types list. Also raises exception if email is in use in any other user table. Also raises exception if ICAO is not recognized.

    Args:
        Session (Session): The database session automatically provided by @with_session
        first_name (str): The first name of the new member of airport staff
        last_name (str): The last name of the new member of airport staff
        email (str): The email of the new member of airport staff
        password (str): The password of the new member of airport staff
        type (str): The type for the new member of airport staff
        assigned_airport_icao (str): The assigned airport ICAO of the new member of airport staff
    """
    LOGGER.info("Adding new airport staff member...")
    LOGGER.debug(f"{first_name = }, {last_name = }, {email = }, {assigned_airport_icao = }")

    # * Validation

    if (
        type(first_name) != str
        or (type(last_name) != str and last_name is not None)
        or len(first_name) > 34
        or len(first_name) < 1
        or len(last_name) > 34
    ):
        LOGGER.error(f"An invalid name has been inputted {first_name = }, {last_name = }")
        raise InvalidNameException

    airport = (
        Session.query(Airport)
        .filter(Airport.icao == assigned_airport_icao)
    ).first()

    if airport == None:
        LOGGER.error("Invalid airport ICAO given.")
        raise InvalidAirportException(assigned_airport_icao)

    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)") # Only checks correct format, does not confirm has not been misstyped of lied about
    if pattern.match(email) == None or len(email) > 124:
        LOGGER.error("Email is invalid format")
        raise InvalidEmailException

    if check_email_already_in_use(Session, email):
        LOGGER.error("The email is already in use")
        raise InvalidEmailException

    if type(password) != str:
        LOGGER.error("Invalid password was given")
        raise InvalidPasswordException

    if staff_type not in AIRPORT_STAFF_TYPES:
        LOGGER.error("Invalid airport staff type given")
        raise StaffException

    # * Processing

    new_staff_member = AirportStaff(first_name=first_name, last_name=last_name, email=email, password=password, staff_type=staff_type, assigned_airport_icao=assigned_airport_icao)
    Session.add(new_staff_member)


@with_session
def edit_airport_staff_member(Session: Session, airport_staff_id: int, first_name: str = None, last_name: str = None, email: str = None, password: str = None, type: str = None, assigned_airport_icao: str = None) -> None:
    """Edits the airport staff record with the given ID. Raises exception if email, or password are invalid format. Also raises exception if type is not in allowed airport staff types list. Also raises exception if email is in use in any other user table. Also raises exception if ICAO is not recognized.
    
        Args:
            Session (Session): The database session automatically provided by @with_session
            airport_staff_id (int): The ID of the airport staff record to edit
            first_name (str): The new first name of the member of airport staff
            last_name (str): The new last name of the member of airport staff
            email (str): The new email of the member of airport staff
            password (str): The new password of the member of airport staff
            type (str): The new type for the member of airport staff
            assigned_airport_icao (str): The new assigned airport ICAO of the member of airport staff
        """

@with_session
def delete_airport_staff(Session: Session, airport_staff_id: int) -> None:
    """Deletes the given member of airport staff.

    Args:
        Session (Session): The database session automatically provided by @with_session
        airport_staff_id (int): The ID of the airport staff member to be deleted
    """
    LOGGER.info("Deleting airport staff member")
    LOGGER.debug(f"{airport_staff_id = }")

    employee = (
        Session.query(AirportStaff)
        .filter(AirportStaff.airport_staff_id == airport_staff_id)
    ).first()

    if employee == None:
        LOGGER.error("Airport staff member does not exist")
        raise ExistenceException

    Session.delete(employee)

@with_session
def get_representative_assigned_guests(Session: Session, representative_id: int) -> list[tuple[int, str, str, datetime]]:
    """Gets the assigned users of the given representative. Raises exception if representative does not exist.

    ## Return Format;
        [
            (
                <guest_id>: int,
                <guest_first_name>: str,
                <guest_last_name>: str,
                <guest_next_flight>: datetime
            )
        ]

    Args:
        Session (Session): The database session automatically provided by @with_session
        representative_id (int): The ID of the representative to retrieve the guest of
    """