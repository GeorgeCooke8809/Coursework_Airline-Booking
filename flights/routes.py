from models.base import with_session
from sqlalchemy.orm import Session

from models import Route, Flight

from datetime import datetime, timedelta

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

@with_session
def get_all_routes(Session: Session) -> list[tuple[int, str, str]]:
    """Gets and returns a list of all route objects regardless of if they have any flights or services

    ## Return Format:
        [
            (
                <route_id>: str
                <departure_airport_name>: str,
                <arrival_airport_name>: str
            )
        ]

    Args:
        Session (Session): The database session automatically provided by @with_session
    """

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

    # TODO: Add more statistics to gather