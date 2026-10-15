from models.base import with_session
from sqlalchemy.orm import Session

from models import Companion
from models import SEX_OPTIONS

from datetime import date

@with_session
def get_all_guest_companions(Session: Session, guest_id: int) -> list[tuple[int, str, date, date, bool]]:
    """Gets a list of all the companions for the given guest. Used in the guest profile page and in the customer support rep portal.

    ## Return Format:
        [
            (
                <companion_id>: int,
                <companion_passport_name>: str,
                <companion_date_of_birth>: date,
                <companion_passport_expiry>: date,
                <companion_favourite>: bool
            )
        ]

    Args:
        Session (Session): The database session automatically provided by @with_session
        guest_id (int): The ID of the guest to retrieve the companions of
    """

@with_session
def add_companion(Session: Session, guest_id: int, passport_name: str, passport_expiry: date, passport_number: str, date_of_birth: date, nationality: str, passport_sex: str, passport_authority: str) -> None:
    """Adds a companion for the given guest with the given details. Raises error if guest does not exist, expiry is before current date, date of birth is after current date, or sex is invalid. Status defaults to active.

    Args:
        Session (Session): The database session automatically provided by @with_session
        guest_id (int): The ID of the guest to attach the companion to.
        passport_name (str): The passport name for the new companion.
        passport_expiry (date): The passport expiry for the new companion.
        passport_number (str): The passport number for the new companion.
        date_of_birth (date): The date of birth for the new companion.
        nationality (str): The nationality for the new companion.
        passport_sex (str): The sex of the new companion.
        passport_authority (str): The passport authority for the new companion.
    """

@with_session
def edit_companion(Session: Session, companion_id: int, passport_name: str = None, passport_expiry: date = None, passport_number: str = None, date_of_birth: date = None, nationality: str = None, passport_sex: str = None, passport_authority: str = None) -> None:
    """Edits a companion. Raises error if guest does not exist, expiry is before current date, date of birth is after current date, or sex is invalid. This is used in the customer support rep portal.
    
    Args:
        Session (Session): The database session automatically provided by @with_session
        companion_id (int): The ID of the companion to edit.
        passport_name (str): The new passport name for the  companion.
        passport_expiry (date): The new passport expiry for the companion.
        passport_number (str): The new passport number for the companion.
        date_of_birth (date): The new date of birth for the companion.
        nationality (str): The new nationality for the companion.
        passport_sex (str): The new sex of the companion.
        passport_authority (str): The new passport authority for the companion.
    """

    # ? Make fail if the companion has already taken a flight - could be used nefariously to change passenger records.

@with_session
def disable_companion(Session: Session, companion_id: int) -> None:
    """Sets the status of the provided companion to inactive

    Args:
        Session (Session): The database session automatically provided by @with_session
        companion_id (int): The ID of the companion to set as inactive
    """

@with_session
def favourite_companion(Session: Session, companion_id: int) -> None:
    """Sets the favourite status of the given companion to True and sets the favourite status of the guest's current favourite companion to False. Raises an exception if the companions expiry is before today or if the companion's status is inactive.

    Args:
        Session (Session): The database session automatically provided by @with_session
        companion_id (int): The companion ID to mark as favourited.
    """