from models.base import with_session
from sqlalchemy.orm import Session
from models import Booking, BookingSeat

from datetime import datetime, timedelta
import logging

LOGGER = logging.getLogger(__name__)

@with_session
def batch_clear_unpaid_bookings(Session: Session) -> None:
    """A regularly run service to delete booking records that have been abandoned (marked as unpaid) > 7 days.

    Args:
        Session (Session): The database session provided automatically with @with_session
    """
    # ? Could add first run prompt user to continue booking - The first time the booking is marked for deletion, it sends an email to the guest promoting them to continue booking.

    abandoned_bookings = (
        Session.query(Booking)
        .filter(Booking.datetime_booked < datetime.now() - timedelta(days=7))
        .filter(Booking.payment_cleared == False)
    ).all()

    for booking in abandoned_bookings:
        Session.query(BookingSeat).filter(BookingSeat.booking_id == booking.booking_id).delete()
        Session.query(Booking).filter(Booking.booking_id == booking.booking_id).delete()