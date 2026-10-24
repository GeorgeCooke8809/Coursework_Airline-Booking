from models.base import with_session
from sqlalchemy.orm import Session

from models import Route, Flight, Airport
from utils import InvalidAirportException

from datetime import datetime, timedelta
import logging

LOGGER = logging.getLogger(__name__)

@with_session
def create_route(Session: Session, departure_airport_icao: str, arrival_airport_icao: str, price: float) -> None:
    """Creates a new route between the given airports and at the given price. Raises exception if airport(s) don't exist, route already exists, or price is negative

    Args:
        Session (Session): The database session automatically provided by @with_session
        departure_airport_icao (str): The ICAO code for the departure airport
        arrival_airport_icao (str): The ICAO code for the arrival airport
        price (float): The price for one seat on flights for the given route
    """
    # ? Switch airports to IDs and get users to select for searchable dropdown

    LOGGER.info("Creating new route...")
    LOGGER.debug(f"{departure_airport_icao = }, {arrival_airport_icao = }, {price = }")

    # * Backend Validation (and setting departure / arrival airports in ORM):

    if departure_airport_icao == arrival_airport_icao:
        logging.exception("Departure and arrival airports are the same")
        raise InvalidAirportException(arrival_airport_icao)

    departure_airport: Airport = (
        Session.query(Airport)
        .filter(Airport.icao == departure_airport_icao)
        .first()
    )

    if departure_airport == None:
        LOGGER.exception("Invalid departure airport given.")
        raise InvalidAirportException(departure_airport_icao)

    arrival_airport: Airport = (
        Session.query(Airport)
        .filter(Airport.icao == arrival_airport_icao)
        .first()
    )

    if arrival_airport == None:
        LOGGER.exception("Invalid arrival airport given.")
        raise InvalidAirportException(arrival_airport_icao)

    if type(price) != float and type(price) != int:
        LOGGER.exception("Invalid price data type given.")
        raise Exception("Invalid price data type entered when creating route")
    if price < 0:
        LOGGER.exception("Invalid price data type given.")
        raise Exception("Invalid price data type entered when creating route")


    # * Adding Record To Database:

    new_route = Route(origin=departure_airport, destination=arrival_airport, price=price)
    Session.add(new_route)

    LOGGER.info("Successfully created new route")

@with_session
def get_all_routes(Session: Session) -> list[tuple[int, str, str]]:
    """Gets and returns a list of all route objects regardless of if they have any flights or services

    ## Return Format:
        [
            (
                <route_id>: int
                <departure_airport_name>: str,
                <arrival_airport_name>: str
            )
        ]

    Args:
        Session (Session): The database session automatically provided by @with_session
    """
    LOGGER.info("Getting all routes...")

    # ? Make get_all_routes order by by most popular / most services - might make it easier for operations managers to find the correct routes faster (on average).

    routes: list[Route] = Session.query(Route).all()

    LOGGER.debug(f"{routes = }")

    to_return = []

    for route in routes:
        to_return.append((route.route_id, route.origin.name, route.destination.name))

    return to_return

@with_session
def generate_route_statistics(Session: Session, route_id: int, timeframe: timedelta) -> dict:
    """Gets statistics for teh given route.

    ## Return Format:
        {
            "averageFlightSaturation": [...],
            "averageFlightSaturationByWeekday": [...]
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        route_id (int): The route to get statistics for
        timeframe (timedelta): The window to look at for statistics e.g.: the past 30 days
    """
    # TODO: Program generate_generate_route_statistics
    # TODO: Add more statistics to gather