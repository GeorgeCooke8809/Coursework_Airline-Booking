from models.base import with_session
from sqlalchemy.orm import Session

from models import Service, Route
from models import SERVICE_REPEAT_TYPES
from utils import RepeatException, InvalidDateException

from datetime import datetime, time, date
import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_route_schedules(Session: Session, route_id: int) -> dict:
    """Gets the schedules/services for the given route where show_in_list is True. Used in flight operations manager portal. Results are split into past and present where past are schedules where the end date is before datetime.now()

    ## Return Format;
        {
            "past": [
                        (
                            <service_id>: int,
                            <service_type>: str,
                            <service_frequency>: int,
                            <service_repeats_on: int,
                            <schedule_time_utc>: time
                        )
                    ]
            "present": [
                        (
                            <service_id>: int,
                            <service_type>: str,
                            <service_frequency>: int,
                            <service_repeats_on: int,
                            <schedule_time_utc>: time
                        )
                    ]
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        route_id (int): The route ID of the route to get schedules for
    """

@with_session
def add_schedule(Session: Session, route_id: int, start_date: date, end_date: date, repeat_type: str, frequency: int, repeats_on: int, time: time) -> None:
    """Creates a new schedule for the given route with the given details. Raises an exception if the repeat type is not allowed from SERVICE_REPEAT_TYPES, if end date is before datetime.now(), if start_date is before datetime.now(), or if repeats_on does not match repeat type

    Args:
        Session (Session): The database session automatically provided by @with_session
        route_id (int): The route ID of the route to make a service for
        start_date (date): The start date of the service/schedule
        end_date (date): The end date of the service/schedule
        type (str): The repeat type of the service/schedule
        frequency (int): The repeat frequency of the service/schedule
        repeats_on (int): The day of the week/month that the service repeats on
        time (time): The time of flight departures for this service/schedule
    """
    LOGGER.info("Adding schedule...")

    # * Validation Checks:

    if repeat_type not in SERVICE_REPEAT_TYPES:
        LOGGER.exception("repeat_type given was invalid")
        raise RepeatException

    if end_date < datetime.today():
        LOGGER.exception("end_date was in the past")
        raise InvalidDateException

    if start_date < datetime.today():
        LOGGER.exception("start_date was in the past")
        raise InvalidDateException

    if end_date < start_date:
            LOGGER.exception("end_date is before start_date")
            raise InvalidDateException

    if (
        (repeat_type == "monthly" and (repeats_on > 31 or repeats_on < 1))
        or (repeat_type == "weekly" and (repeats_on > 7 or repeats_on < 1))
    ):
         LOGGER.exception("Invalid repeat_type and repeats_on combination")
         raise RepeatException

    # * Processing:

    if repeat_type == "daily":
         repeats_on = None

    new_schedule = Service(route_id = route_id, start_date = start_date, end_data = end_date, repeat_type = repeat_type, repeat_frequency = frequency, repeats_on = repeats_on, repeat_time_utc = time, show_in_list = True)
    Session.add(new_schedule)

@with_session
def edit_schedule(Session: Session, service_id: int, end_date: date = None, type: str = None, frequency: int = None, repeats_on: int = None, time: time = None) -> None:
    """Edits the given service with the given details. Raises an exception if the repeat type is not allowed from SERVICE_REPEAT_TYPES or if repeats_on does not match repeat type

    Args:
        Session (Session): The database session automatically provided by @with_session
        service_id (int): The service ID to edit
        end_date (date): The end date of the service/schedule
        type (str): The repeat type of the service/schedule
        frequency (int): The repeat frequency of the service/schedule
        repeats_on (int): The day of the week/month that the service repeats on
        time (time): The time of flight departures for this service/schedule
    """

@with_session
def delete_schedule(Session: Session, service_id: int) -> None:
    """Deletes the given service. Does not delete any flights already created for it.

    Args:
        Session (Session): The database session automatically provided by @with_session
        service_id (int): The ID of the service to be deleted
    """