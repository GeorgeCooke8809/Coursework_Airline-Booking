from models.base import with_session
from sqlalchemy.orm import Session
from models import Guest, Flight, Booking

from datetime import datetime
import pytz

@with_session
def create_unpaid_booking(Session: Session, guest_id: int, flight_id: int):
    """Creates a new booking for the given user and flight. Should be called when going from flight selection page to seat selection. Is not shown as a booking for the user in their profile page until paid for. Adds a new database record to 'bookings' table with autoincrement ID, given user ID, given flight ID, datetime.now() for booking datetime, False for paid
    Results could potentially be used to prompt a user to continue process if never completed (abandoned basket).

    Args:
        Session (Session): The database session automatically provided with @with_session
        guest_id (int): The guest ID that the booking should be created for.
        flight_id (int): The flight ID that the booking should be linked to.
    """