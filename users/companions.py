from models.base import with_session
from sqlalchemy.orm import Session

from models import Companion, Guest
from models import SEX_OPTIONS

from utils import ExistenceException, PassportException, CompanionException

from datetime import date
import logging

LOGGER = logging.getLogger(__name__)

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

    LOGGER.info("Getting list of all guest companions...")
    LOGGER.debug(f"{guest_id = }")

    guest = (
        Session.query(Guest)
        .filter(Guest.guest_id == guest_id)
    ).first()

    if guest is None:
        LOGGER.error("Guest does not exist")
        raise ExistenceException

    to_return = []

    for companion in guest.companions:
        to_return.append((
            companion.companion_id,
            companion.passport_name,
            companion.date_of_birth,
            companion.passport_expiry,
            companion.favorite
        ))

    return to_return

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
    LOGGER.info("Adding new companion...")
    LOGGER.debug(f"{guest_id = }, {passport_name = }, {passport_expiry = }, {passport_number = }, {date_of_birth = }, {nationality = }, {passport_sex = }, {passport_authority = }")

    # * Validation:

    guest = (
        Session.query(Guest)
        .filter(Guest.guest_id == guest_id)
    ).first()

    if guest == None:
        LOGGER.error("Guest does not exist")
        raise ExistenceException

    if (
        type(passport_name) != str
        or len(passport_name) > 38
        or passport_name == ""
        or type(passport_expiry) != date
        or passport_expiry < date.today()
        or type(passport_number) != str
        or len(passport_number) > 9
        or passport_number == ""
        or type(date_of_birth) != date
        or date_of_birth > date.today()
        or type(nationality) != str
        or nationality == ""
        or passport_sex not in SEX_OPTIONS
        or type(passport_authority) != str
        or passport_authority == ""
    ): # ? Split passport validation into multiple validation statements and exceptions
        LOGGER.error("There is something wrong with the passport details given")
        raise PassportException

    # * Processing

    companion_favourite = False

    if len(guest.companions) == 0:
        companion_favourite = True

    new_companion = Companion(guest_id=guest_id, passport_name=passport_name, passport_number=passport_number, passport_expiry=passport_expiry, nationality=nationality, passport_issue_authority=passport_authority, date_of_birth=date_of_birth, sex=passport_sex, status="active", favorite=companion_favourite) # TODO: Fix favourite UK spelling

    Session.add(new_companion)

@with_session
def edit_companion(Session: Session, companion_id: int, passport_name: str = None, passport_expiry: date = None, passport_number: str = None, date_of_birth: date = None, nationality: str = None, passport_sex: str = None, passport_authority: str = None) -> None:
    """Edits a companion. Raises exception if companion does not exist, expiry is before current date, date of birth is after current date, or sex is invalid. This is used in the customer support rep portal.
    
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

    # ? Make fail if the companion has already taken a flight - could be used nefariously to change passenger records if not done

@with_session
def disable_companion(Session: Session, companion_id: int) -> None:
    """Sets the status of the provided companion to inactive

    Args:
        Session (Session): The database session automatically provided by @with_session
        companion_id (int): The ID of the companion to set as inactive
    """
    LOGGER.info("Disabling companion")
    LOGGER.debug(f"{companion_id = }")

    companion = (
        Session.query(Companion)
        .filter(Companion.companion_id == companion_id)
    ).first()

    if companion is None:
        LOGGER.error("Companion does not exist")
        raise ExistenceException

    companion.status = "inactive"

@with_session
def favourite_companion(Session: Session, companion_id: int) -> None:
    """Sets the favourite status of the given companion to True and sets the favourite status of the guest's current favourite companion to False. Raises an exception if the companions expiry is before today or if the companion's status is inactive.

    Args:
        Session (Session): The database session automatically provided by @with_session
        companion_id (int): The companion ID to mark as favourited.
    """
    LOGGER.info("Setting companion to favourite")
    LOGGER.debug(f"{companion_id = }")

    companion = (
        Session.query(Companion)
        .filter(Companion.companion_id == companion_id)
    ).first()

    if companion is None:
        LOGGER.error("Companion does not exist")
        raise ExistenceException

    if companion.passport_expiry < date.today():
        LOGGER.error("The companions passport is expired so they cannot be added as favourite")
        raise CompanionException

    if companion.status != "active":
        LOGGER.error("The companion is inactive and so cannot be marked as favourite")
        raise CompanionException

    guest = companion.guest

    current_favourite = (
        Session.query(Companion)
        .filter(Companion.guest_id == guest.guest_id)
        .filter(Companion.favorite == True)
    ).first()

    if current_favourite is not None:
        current_favourite.favorite = False

    companion.favorite = True