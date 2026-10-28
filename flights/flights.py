from models.base import with_session
from sqlalchemy.orm import Session

from models import Flight, Airport, Service, Route
from models import FLIGHT_STATUS_OPTIONS
from utils.exceptions import InvalidDateException, ExistenceException, FlightStatusException, InvalidAirportException

from .schedules import add_schedule

from datetime import datetime, timedelta, date, UTC
import logging
from random import randint
from math import radians, cos, sqrt

LOGGER = logging.getLogger(__name__)

BATCH_GENERATE_LOOK_AHEAD = 90 # The number of days ahead of datetime.today() the batch generate flights will look ahead to create
AIRCRAFT_AVG_SPEED_MPH = 520 # ? Different planes have different speeds

@with_session
def get_airport_flights(Session: Session, airport_icao: str) -> list[tuple[str, str, str, str, datetime, datetime]]:
    """Gets a list of all of the flights departing from the provided airport in the next 24 hours. Typically used in the gate agent and check in agent portals.

    ## Return Format:
    [
        (
            <flight_number>: str,
            <destination_icao>: str,
            <destination_name>: str,
            <departure_time>: str,
            <check_in_close_datetime>: datetime,
            <gate_close_datetime>: datetime
        )
    ]

    Args:
        Session (Session): The database session object automatically provided by @with_session
        airport_icao (str): The airport ICAO to get flights from
    """
    LOGGER.info("Getting airport flights")
    LOGGER.debug(f"{airport_icao = }")

    # * Validation

    airport = (
        Session.query(Airport)
        .filter(Airport.icao == airport_icao)
    ).first()

    if airport == None:
        LOGGER.error("Airport does not exist")
        raise InvalidAirportException(airport_icao)

    # * Processing
    routes = [route.route_id for route in airport.departures]

    LOGGER.debug(f"{routes = }")

    today = date.today()

    active_services = (
        Session.query(Service)
        .filter(Service.route_id.in_(routes))
        .filter(Service.start_date <= today)
        .filter(Service.end_date >= today)
    ).all()

    LOGGER.debug(f"{active_services = }")

    service_ids = [service.service_id for service in active_services]

    departures = (
        Session.query(Flight)
        .filter(Flight.service_id.in_(service_ids))
        .filter(Flight.scheduled_departure_datetime_utc <= datetime.now(tz=UTC) + timedelta(days=1))
        .filter(Flight.status == "scheduled")
        .order_by(Flight.scheduled_departure_datetime_utc)
    ).all()

    LOGGER.debug(f"{departures = }")

    return_array = []

    for flight in departures:
        destination = flight.service.route.destination

        departure_time = flight.scheduled_departure_datetime_utc.strftime("%H:%M")
        check_in_close_time = flight.scheduled_departure_datetime_utc - timedelta(minutes=30) # ? Different check in close time for different flights
        gate_close_time = flight.scheduled_departure_datetime_utc - timedelta(minutes=90) # ? Different gate close time for different flights

        return_array.append((
            flight.flight_number,
            destination.icao,
            destination.name,
            departure_time,
            check_in_close_time,
            gate_close_time
        ))

    return return_array


@with_session
def change_flight_status(Session: Session, flight_id: int, new_status: str) -> None:
    """Changes the status of the given flight to the given new status

    Args:
        Session (Session): The database session automatically provided by @with_session
        flight_id (int): The flight_id of the flight to be updated
        new_status (str): The new status of the flight. Returns error if not in ("scheduled", "departed", "cancelled")
    """
    LOGGER.info("Changing flight status...")
    LOGGER.debug(f"{flight_id = }, {new_status = }")

    # * Validation

    flight = (
        Session.query(Flight)
        .filter(Flight.flight_id == flight_id)
    ).first()

    if flight == None:
        LOGGER.error("Flight does not exist")
        raise ExistenceException

    if new_status not in FLIGHT_STATUS_OPTIONS:
        LOGGER.error("Invalid flight status given")
        raise FlightStatusException

    # * Processing
    flight.status = new_status

@with_session
def get_flight_details(Session: Session, flight_id: int, airport_staff_id: int) -> dict:
    """Gets the flight details for the selected flight. Used by check-in and get agent portals.

    ## Return Format:
        {
            "flightNo": <flight_number>: str,
            "totalPassengers": <total_passengers>: int,
            "checked": <check_passengers_total>: int,
            "boarded" <boarded_passengers_total>: int,
            "status": <status>: str,
            "departureTime": <departure_datetime>: datetime,
            "checkInCloseTime": <check_in_close_datetime>: datetime,
            "gateCloseTime": <gate_close_datetime>: datetime,
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        flight_id (int): The flight number to get details for
        airport_staff_id (int): The airport staff ID the request is coming from to ensure they have access to that flight
    """

    # TODO: Write get_get_flight_details - waiting on booking seats

@with_session
def get_route_flights(Session: Session, route_id: int) -> dict:
    """Returns a list of past and future flights for the given route_id. Used in the flight operations manager portal

    ## Return Format:
        {
            "past": [
                        (
                            <flight_id>: int
                            <departure_datetime>: datetime,
                            <capacity>: int,
                            <booking_quantity>: int,
                            <status>: str
                        )
                    ]
            "future": [
                        (
                            <flight_id>: int
                            <departure_datetime>: datetime,
                            <capacity>: int,
                            <booking_quantity>: int,
                            <status>: str
                        )
                    ]
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        route_id (int): The route ID to search for flights for
    """
    # Will have to join tables?
    # TODO: Write get_route_flights - waiting on booking seats
    # ? Split into past and present if flight quantities get too high for quick retrieval. Only pull past (with pagination) on button press

@with_session
def edit_flight_departure_time(Session: Session, flight_id: int, new_departure_datetime: datetime) -> None:
    """Edit the departure time of the given flight_id. Raises exception if flight is already departed or new departure time is in the past.

    Args:
        Session (Session): The database session automatically provided by @with_session
        flight_id (int): The flight ID of the flight to be edited
        new_departure_time (datetime): The new departure datetime for the flight
    """
    LOGGER.info("Changing flight departure time...")
    LOGGER.debug(f"{flight_id = }, {new_departure_datetime = }")

    # * Validation

    flight = (
        Session.query(Flight)
        .filter(Flight.flight_id == flight_id)
    ).first()

    if flight == None:
        LOGGER.error("Flight does not exist")
        raise ExistenceException

    if flight.status != "scheduled":
        LOGGER.error(f"This operation cannot be performed on this flight. It's status is {flight.status}")
        raise FlightStatusException

    if not isinstance(new_departure_datetime, datetime) or new_departure_datetime < datetime.now(tz=UTC):
        LOGGER.error("New departure time is invalid")
        raise InvalidDateException

    # * Processing
    flight.scheduled_departure_datetime_utc = new_departure_datetime

@with_session
def add_new_flight(Session: Session, service_id: int, scheduled_departure_utc: datetime) -> None:
    """Creates a new flight with the given service ID and scheduled departure datetime. Flight number is autogenerated, datetime created is set to datetime.now(), status is set to scheduled. Raises exception if scheduled departure is before now.
    This will be used by the batch add and add_one_off to create a flight on a given datetime. The time will always match the time in the service but can updated by the user.

    Args:
        Session (Session): The database session automatically provided by @with_session
        service_id (int): The service ID for the flight to be attached to.
        scheduled_departure_utc (datetime): The scheduled departure for the flight in UTC. **Must have tzinfo = UTC**
    """
    LOGGER.info("Creating new flight...")
    LOGGER.debug(f"{service_id = }, {scheduled_departure_utc = }")

    # * Validation

    service = (
        Session.query(Service)
        .filter(Service.service_id == service_id)
    ).first()

    if service == None:
        LOGGER.error("Service does not exist")
        raise ExistenceException

    if not isinstance(scheduled_departure_utc, datetime) or scheduled_departure_utc < datetime.now(tz=UTC):
        LOGGER.error("Scheduled departure is before now or of an invalid type, cannot create.")
        raise InvalidDateException

    # ? Match time of departure to service time?

    # * Processing
    flight_no = randint(1, 9999)
    flight_no = str(flight_no).rjust((len(str(flight_no))) + 4, "0")
    datetime_created = datetime.now(tz=UTC)
    status = "scheduled"

    new_flight = Flight(service_id=service_id, flight_number=flight_no, scheduled_departure_datetime_utc=scheduled_departure_utc, datetime_created_utc=datetime_created, status=status)

    Session.add(new_flight)

    LOGGER.info("Finished adding new flight.")


@with_session
def add_one_off_flight(Session: Session, route_id: int, scheduled_departure_utc: datetime) -> None:
    """Creates a one off flight for the given route and time. Starts by creating new daily schedule with start and end date the same then creates a new flight attached to it.

    Args:
        Session (Session): The database session automatically provided by @with_session
        route_id (int): The route ID to make a one off flight for
        scheduled_departure_utc (datetime): Teh scheduled departure time of the flight, put into the service record. **Must have tzinfo = UTC**
    """
    LOGGER.info("Creating one-off flight...")
    LOGGER.debug(f"{route_id = }, {scheduled_departure_utc = }")

    # * Validation:
    route = (
        Session.query(Route)
        .filter(Route.route_id == route_id)
    ).first()

    if route == None:
        LOGGER.error("Route does not exist")
        raise ExistenceException

    if not isinstance(scheduled_departure_utc, datetime) or scheduled_departure_utc < datetime.now(tz=UTC):
        LOGGER.error("Scheduled departure is before now or of an invalid type, cannot create.")
        raise InvalidDateException

    # * Processing
    service_id = add_schedule(Session, route_id, scheduled_departure_utc.date(), scheduled_departure_utc.date(), "daily", 1, scheduled_departure_utc.time(), shown_in_list = False)

    LOGGER.debug("Successfully created new service/schedule")

    add_new_flight(Session, service_id, scheduled_departure_utc)

    LOGGER.info("Successfully added one-off flight")


@with_session
def batch_generate_scheduled_flights(Session: Session):
    """Batch generates flights that haven't already been created for schedules. Uses BATCH_GENERATE_LOOK_AHEAD constant for how far ahead to look.

    Args:
        Session (Session): The database session automatically provided by @with_session
    """

@with_session
def search_for_flight(Session: Session, departure_airport: str, arrival_airport: str, date: date) -> list:
    """Searches for a flight that matches the given criteria. Uses like to get close matches for airport name.

    ## Return Format:
        [
            (
                <departure_airport_name>: str,
                <departure_airport_iata>: str,
                <departure_datetime>: datetime,
                <flight_duration>: timedelta,
                <destination_airport_name>: str,
                <destination_airport_iata>: str,
                <arrival_time>: datetime,
                <seat_price>: float
            )
        ]

    Args:
        Session (Session): The database session automatically provided by @with_session
        departure_airport (str): The search term for the name of the departure airport
        arrival_airport (str): The search term for the name of the arrival airport
        date (date): The date that flights should be on
    """
    # ? Switch airports to IDs and make users select specific airport in UI

def calculate_flight_duration(Session: Session, flight_id: int) -> timedelta:
    """Uses the flight ID to first get route, then coordinates of departure and arrival airports. This is used with pythagoras to get the route length in coordinate units. This is converted to miles at the equator and divided by cruise speed of aircraft to estimate flight duration.

    Args:
        Session (Session): The database session. Must be provided by the calling function.
        flight_id (int): Teh flight ID to calculate the duration of.
    """
    # ? Different weather conditions will impact ground speed
    # ? Different aircraft will have different cruise speeds

    # One longitude degree at equator = 69.172 miles
    # Longitude degree = cos(latitude (radians)) * longitude at equator

    # Latitude degree = 69 miles

    LOGGER.info("Getting flight duration")
    LOGGER.debug(f"{flight_id = }")

    # * Validation:
    flight = (
        Session.query(Flight)
        .filter(Flight.flight_id == flight_id)
    ).first()

    if flight == None:
        LOGGER.error("Flight does not exist")
        raise ExistenceException

    # * Processing
    route = flight.service.route

    origin = route.origin
    origin_lat = origin.latitude
    origin_lon = origin.longitude

    destination = route.destination
    destination_lat = destination.latitude
    destination_lon = destination.longitude

    lat_delta = origin_lat - destination_lat
    lat_delta_miles = lat_delta * 69

    average_latitude = radians((origin_lat + destination_lat) / 2)

    lon_delta = origin_lon - destination_lon
    lon_delta_miles = cos(average_latitude) * 69.172 * lon_delta

    hypotenuse = sqrt(lon_delta_miles ** 2 + lat_delta_miles ** 2)

    hours = hypotenuse / AIRCRAFT_AVG_SPEED_MPH

    return timedelta(hours=hours)


@with_session
def calculate_seat_price(Session: Session, flight_id: int, number_of_seats: int = 1) -> float:
    """Calculates the price for a seat. Used for the search_for_flight function as well as updating price when selecting seats.

    Args:
        Session (Session): The database session automatically provided by @with_session.
        flight_id (int): The flight to calculate the price of
        number_of_seats (int): The number of seats to calculate the price of
    """
    # ? Surge/dynamic pricing
    # ? Different flights on a route can have different prices

    LOGGER.info("Getting seat price...")
    LOGGER.debug(f"{flight_id = }, {number_of_seats = }")

    # * Validation

    flight = (
        Session.query(Flight)
        .filter(Flight.flight_id == flight_id)
    ).first()

    if flight == None:
        LOGGER.error("Flight does not exist")
        raise ExistenceException

    if type(number_of_seats) != int or number_of_seats <= 0:
        LOGGER.error("Invalid number of seats given")
        raise Exception

    # * Processing
    route = flight.service.route

    LOGGER.info(f"Seat Price = {route.price}")

    return float(route.price * number_of_seats)

# ? Similar flights search
# ? Layover flights search