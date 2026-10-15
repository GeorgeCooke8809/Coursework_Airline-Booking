from models.base import with_session
from sqlalchemy.orm import Session

from models import Guest, Booking, BookingSeat

from datetime import datetime, timedelta

@with_session
def get_all_guest_bookings(Session: Session, user_id: int) -> dict:
    """Gets a list of all past and present bookings for the user and returns details. Bookings are ordered by datetime of departure.
    #### Return Format:
    {
        "past": [
                (
                    <booking_id>: int,
                    <departure_airport_name>: str,
                    <departure_airport_iata>: str,
                    <departure_local_datetime>: datetime,
                    <arrival_airport_name>: str,
                    <arrival_airport_iata>: str,
                    <arrival_local_datetime>
                    <flight_duration>: timedelta,
                    <number_of_companions>: int
                )
            ],
        "future": [
                (
                    <booking_id>: int,
                    <departure_airport_name>: str,
                    <departure_airport_iata>: str,
                    <departure_local_datetime>: datetime,
                    <arrival_airport_name>: str,
                    <arrival_airport_iata>: str,
                    <arrival_local_datetime>
                    <flight_duration>: timedelta,
                    <number_of_companions>: int
                )
            ]
    }

    Args:
        Session (Session): The database session automatically created by @with_session
        user_id (int): The user ID for the query
    """