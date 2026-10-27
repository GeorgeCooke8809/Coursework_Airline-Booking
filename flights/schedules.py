from models.base import with_session
from sqlalchemy.orm import Session

from models import Service, Route
from models import SERVICE_REPEAT_TYPES
from utils import RepeatException, InvalidDateException, ExistenceException, InvalidTimeException

from datetime import time, date
import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_route_schedules(Session: Session, route_id: int) -> dict:
    """Gets the schedules/services for the given route where show_in_list is True. Used in flight operations manager portal. Results are split into past and present where past are schedules where the end date is before datetime.now(). Past schedules are ordered by end date and present schedules are ordered by start date.

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
                    ],
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
    LOGGER.info("Getting route schedules...")
    LOGGER.debug(f"{route_id = }")

    # * Validation

    route = (
        Session.query(Route)
        .filter(Route.route_id == route_id)
    ).first()

    if route == None:
        LOGGER.error("Route does not exist.")
        raise ExistenceException

    # * Selecting functionality

    past_schedules = (
        Session.query(Service)
        .filter(Service.route_id == route_id)
        .filter(Service.end_date < date.today())
        .order_by(Service.end_date)
    ).all()

    past_schedules_array = []
    for schedule in past_schedules: past_schedules_array.append((schedule.service_id, schedule.repeat_type, schedule.repeat_frequency, schedule.repeats_on, schedule.repeat_time_utc))


    present_schedules = (
        Session.query(Service)
        .filter(Service.route_id == route_id)
        .filter(Service.end_date >= date.today())
        .order_by(Service.start_date)
    ).all()

    present_schedules_array = []
    for schedule in present_schedules: present_schedules_array.append((schedule.service_id, schedule.repeat_type, schedule.repeat_frequency, schedule.repeats_on, schedule.repeat_time_utc))

    return_dict = {
        "past": past_schedules_array,
        "present": present_schedules_array
    }

    LOGGER.debug(f"{return_dict = }")

    return return_dict


@with_session
def add_schedule(Session: Session, route_id: int, start_date: date, end_date: date, repeat_type: str, frequency: int, repeat_time: time, repeats_on: int = None, shown_in_list: bool = True) -> int:
    """Creates a new schedule for the given route with the given details. Raises an exception if the repeat type is not allowed from SERVICE_REPEAT_TYPES, if end date is before datetime.now(), if start_date is before datetime.now(), or if repeats_on does not match repeat type

    Returns ID of new schedule as an int

    Args:
        Session (Session): The database session automatically provided by @with_session
        route_id (int): The route ID of the route to make a service for
        start_date (date): The start date of the service/schedule
        end_date (date): The end date of the service/schedule
        repeat_type (str): The repeat type of the service/schedule
        frequency (int): The repeat frequency of the service/schedule
        repeats_on (int): The day of the week/month that the service repeats on
        repeat_time (time): The time of flight departures for this service/schedule
    """
    LOGGER.info("Adding schedule...")
    LOGGER.debug(f"{route_id = }, {start_date = }, {end_date = }, {repeat_type = }, {frequency = }, {repeat_time = }, {repeats_on = }")

    # * Validation Checks:
    route = (
    Session.query(Route)
    .filter(Route.route_id == route_id)
    ).first()

    if route == None:
        LOGGER.error("Route does not exist.")
        raise ExistenceException

    if repeat_type not in SERVICE_REPEAT_TYPES:
        LOGGER.error("repeat_type given was invalid")
        raise RepeatException

    if type(start_date) != date or type(end_date) != date:
        LOGGER.error("An invalid date data type was given")
        raise InvalidDateException

    if start_date < date.today():
        LOGGER.error("start_date was in the past")
        raise InvalidDateException

    if end_date < start_date:
            LOGGER.error("end_date is before start_date")
            raise InvalidDateException

    if (
        (repeat_type == "monthly" and repeats_on not in range(1, 32))
        or (repeat_type == "weekly" and repeats_on not in range(1, 8))
    ):
        LOGGER.error("Invalid repeat_type and repeats_on combination")
        raise RepeatException

    if not isinstance(repeat_time, time):
        LOGGER.error("Invalid repeat_time was given")
        raise InvalidTimeException

    if type(shown_in_list) != bool:
        LOGGER.error("Shown in list is of invalid type")
        raise Exception

    # * Processing:

    if repeat_type == "daily":
        if repeats_on != None:
            LOGGER.warning(f"Repeat type is daily but repeats_on was given as {repeats_on}. Resetting to None.")
        repeats_on = None

    new_schedule = Service(route_id = route_id, start_date = start_date, end_date = end_date, repeat_type = repeat_type, repeat_frequency = frequency, repeats_on = repeats_on, repeat_time_utc = repeat_time, shown_in_list = shown_in_list)
    Session.add(new_schedule)
    Session.flush()

    LOGGER.info("Successfully created new schedule.")

    return new_schedule.service_id


@with_session
def edit_schedule(Session: Session, service_id: int, end_date: date = None, repeat_type: str = None, frequency: int = None, scheduled_time: time = None, repeats_on: int = None) -> None:
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
    LOGGER.info("Updating schedule...")
    LOGGER.debug(f"{service_id = }, {end_date = }, {repeat_type = }, {frequency = }, {repeats_on = }, {scheduled_time = }")

    # * Validation
    service: Service = (
        Session.query(Service)
        .filter(Service.service_id == service_id)
    ).first()

    if service == None:
        LOGGER.error("Service does not exist to update.")
        raise ExistenceException

    if (repeat_type not in SERVICE_REPEAT_TYPES) and repeat_type != None:
        LOGGER.error("Invalid service repeat type.")
        raise RepeatException

    if type(end_date) != date and end_date != None:
        LOGGER.error("An invalid date data type was given")
        raise InvalidDateException
    
    if frequency != None and (type(frequency) != int or frequency < 1):
        LOGGER.error("An invalid frequency was given")
        raise RepeatException
    
    if type(repeats_on) != int and repeats_on != None:
        LOGGER.error("Invalid repeats_on datatype.")
        raise RepeatException
    elif repeats_on != None:
        if repeat_type == None:
            repeat_type = service.repeat_type

        if repeat_type == "daily" and  repeats_on != None:
            LOGGER.error("Repeats_on was given when repeat_type is daily")
            raise RepeatException
        elif repeat_type == "weekly" and repeats_on not in range(1, 8):
            LOGGER.error("Repeats_on outside of weekly range")
            raise RepeatException
        elif repeat_type == "monthly" and repeats_on not in range(1, 32):
            LOGGER.error("Repeats_on outside of monthly range")
            raise RepeatException
        
    if not isinstance(scheduled_time, time) and scheduled_time != None:
        LOGGER.error("Invalid repeat_time was given")
        raise InvalidTimeException

    # * Processing
    if repeat_type != None:
        service.repeat_type = repeat_type

    if end_date != None:
        service.end_date = end_date

    if frequency != None:
        service.repeat_frequency = frequency

    if repeats_on != None:
        service.repeats_on = repeats_on

    if scheduled_time != None:
        service.repeat_time_utc = scheduled_time

@with_session
def delete_schedule(Session: Session, service_id: int) -> None:
    """Deletes the given service. Does not delete any flights already created for it. Raises exception if does not exist.

    Args:
        Session (Session): The database session automatically provided by @with_session
        service_id (int): The ID of the service to be deleted
    """
    LOGGER.info("Deleting schedule/service")
    LOGGER.debug(f"{service_id = }")

    schedule = (
        Session.query(Service)
        .filter(Service.service_id == service_id)
    ).first()

    if schedule == None: # Also covers if service_id is of invalid type as it will still return None
        LOGGER.error("Schedule does not exist to delete.")
        raise ExistenceException

    Session.query(Service).filter(Service.service_id == service_id).delete()

    LOGGER.info("Successfully deleted service.")