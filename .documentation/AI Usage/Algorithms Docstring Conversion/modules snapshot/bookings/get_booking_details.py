from models.base import with_session
from sqlalchemy.orm import Session

from models import Booking, Companion, Flight, BookingSeat

from datetime import datetime, timedelta, date

@with_session
def get_booking_details(Session: Session, booking_id: int) -> dict:
    """Gets and returns all of the details for thw given booking.

    ## Return Format:
        {
            "departureDatetime": <flight_departure_time>: datetime,
            "flightDuration": <flight_duration>: timedelta,
            "companions": [
                (
                    <companion_passport_name>: str,
                    <companion_date_of_birth>: date,
                    <booking_seat_id>: str
                )
            ]
        }

    Args:
        Session (Session): The database session automatically provided by @with_session
        booking_id (int): The booking ID to get details from
    """