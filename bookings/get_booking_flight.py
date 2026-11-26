from sqlalchemy.orm import Session

from models import Booking, Flight
from models.base import with_session

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_booking_flight(session: Session, booking_id: int):
    flight_id = (
        session.query(Booking.flight_id)
        .filter(Booking.booking_id == booking_id)
    ).first()

    LOGGER.debug(f"{flight_id[0] = }")

    return flight_id[0]