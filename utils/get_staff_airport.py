from sqlalchemy.orm import Session

from models.base import with_session
from models import Airport, AirportStaff

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def get_staff_airport(session: Session, staff_id: int) -> str:
    """Gets and returns the ICAO code of the assigned airport for the given staff menber

    Args:
        session (Session): The SQLalchmey session automatically provided by the with_session wrapper
        staff_id (int): The ID of the staff member to get the airport of

    Returns:
        str: The ICAO code for the airport e.g.: 'EGLL'
    """

    airport_icao = (
        session.query(AirportStaff.assigned_airport_icao)
        .filter(AirportStaff.airport_staff_id == staff_id)
    ).first()[0]

    return airport_icao