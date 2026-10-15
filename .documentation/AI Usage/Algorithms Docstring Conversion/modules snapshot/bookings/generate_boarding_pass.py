from models.base import with_session
from sqlalchemy.orm import Session
from models import Booking, BookingSeat, Companion

import reportlab

@with_session
def generate_boarding_pass(Session: Session, booking_id: int) -> None:
    """Generates a PDF boarding pass of name "boarding.pdf" in the root project directory for the given booking. Overwrites any existing document.

    Args:
        Session (Session): Database session automatically provided by @with_session
        booking_id (int): The bookings ID for the PDF boarding pass to be based on
    """