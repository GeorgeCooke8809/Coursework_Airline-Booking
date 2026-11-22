from sqlalchemy import func, case, or_
from sqlalchemy.orm import Session

from models.base import with_session
from models import Airport

import logging

LOGGER = logging.getLogger(__name__)

@with_session
def search_airport(session: Session, search_term: str):
    LOGGER.info("Searching for airport...")
    LOGGER.debug(f"{search_term = }")
    search_term = search_term.strip()
    
    airport_rank = case(
        (func.upper(Airport.iata) == search_term.upper(), 0),
        (func.lower(Airport.name) == search_term.lower(), 1),
        (Airport.name.ilike(f"%{search_term}%"), 2),
        (Airport.iata.ilike(f"%{search_term}%"), 3),
        else_=4,
    )

    airports = (
        session.query(Airport)
        .filter(Airport.iata != None)
        .filter(or_(
            Airport.name.like(f"%{search_term}%"),
            Airport.iata.like(f"%{search_term}%")
        ))
        .order_by(airport_rank)
    ).all()

    LOGGER.debug(f"{airports = }")

    return [(airport.iata, airport.name) for airport in airports] # Convert into a list of tuples instead of SQLalchemy objects