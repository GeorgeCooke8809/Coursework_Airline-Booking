from models.base import with_session
from sqlalchemy.orm import Session

from models import Guest, AirlineEmployee, AirportStaff

@with_session
def check_login_details(Session: Session, email: str, password: str) -> dict:
    """Checks the login details provided. If details are correct, a dictionary with user ID and type is returned. If login details are incorrect, None is provided. Raises exception if email is used in multiple user databases.

    ## Return Format:
        {
            "id": <user_id>: int,
            "type": <user_table> str = "guest" | "airline" | "airport"
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        email (str): The email of the user to check against
        password (str): The password to check against
    """