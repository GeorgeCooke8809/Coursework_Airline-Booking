from models.base import with_session
from sqlalchemy.orm import Session

from models import AirportStaff, AirlineEmployee, Guest, Booking, Flight
from models import AIRLINE_EMPLOYEE_TYPES, AIRPORT_STAFF_TYPES

from datetime import datetime

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
def add_airline_employee(Session: Session, first_name: str, last_name: str, email: str, phone: str, password: str, type: str) -> None:
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

@with_session
def add_airport_staff(Session: Session, first_name: str, last_name: str, email: str, password: str, type: str, assigned_airport_icao: str) -> None:
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