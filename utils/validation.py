from models.base import with_session
from sqlalchemy.orm import Session

from models import AirportStaff, AirlineEmployee, Guest, Airport

@with_session
def check_email_already_in_use(session: Session, email: str) -> bool:
    for model in (AirlineEmployee, AirportStaff, Guest):
        user = (
            session.query(model)
            .filter(model.email == email)
        ).first()

        if user != None:
            return True

    return False

@with_session
def check_airport_exists(session: Session, icao: str) -> bool:
    airport = (
        session.query(Airport)
        .filter(Airport.icao == icao)
    ).first()

    if airport == None:
        return False

    return True